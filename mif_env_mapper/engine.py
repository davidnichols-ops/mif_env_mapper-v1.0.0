"""
Discovery Engine Module
Queries native package ecosystems across supported platforms.
"""

import os
import sys
import platform
import subprocess
from typing import Dict, List, Optional, Tuple
from .config import SUPPORTED_PLATFORMS, DISTRO_PACKAGE_MANAGERS


class DiscoveryEngine:
    """
    Queries native package ecosystems on Linux (Debian/RedHat/Arch) and Darwin/macOS.
    
    Methods:
        execute_command(args): Defensively executes system processes
        gather_packages(os_type): Drives low-level collection based on OS
        _get_linux_distro(): Detects specific Linux distribution
        get_system_info(): Collects basic system metadata
    """
    
    def __init__(self, timeout: int = 30):
        """
        Initialize the discovery engine.
        
        Args:
            timeout: Maximum seconds to wait for subprocess commands
        """
        self.timeout = timeout
        self._errors: List[str] = []
    
    @property
    def errors(self) -> List[str]:
        """Returns list of non-fatal errors encountered during discovery."""
        return self._errors.copy()
    
    def execute_command(self, args: List[str]) -> List[str]:
        """
        Executes system processes defensively, handling errors gracefully.
        
        Args:
            args: Command and arguments as a list (NEVER use shell=True)
            
        Returns:
            List of stripped stdout lines, empty list on failure
        """
        try:
            result = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                timeout=self.timeout
            )
            return [line.strip() for line in result.stdout.splitlines() if line.strip()]
        except subprocess.TimeoutExpired:
            self._errors.append(f"Command timed out: {' '.join(args)}")
            return []
        except subprocess.CalledProcessError as e:
            self._errors.append(f"Command failed ({e.returncode}): {' '.join(args)}")
            return []
        except FileNotFoundError:
            self._errors.append(f"Command not found: {args[0]}")
            return []
        except PermissionError:
            self._errors.append(f"Permission denied: {' '.join(args)}")
            return []
    
    def _get_linux_distro(self) -> Optional[str]:
        """
        Detects the specific Linux distribution.
        
        Returns:
            Distro identifier string or None if detection fails
        """
        # Try /etc/os-release first (modern standard)
        if os.path.exists("/etc/os-release"):
            try:
                with open("/etc/os-release", "r") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("ID="):
                            distro = line[3:].strip('"').lower()
                            return distro
            except (IOError, PermissionError):
                pass
        
        # Fallback: try lsb_release command
        lsb_output = self.execute_command(["lsb_release", "-si"])
        if lsb_output:
            return lsb_output[0].lower()
        
        return None
    
    def gather_packages(self, os_type: str) -> Dict[str, List[str]]:
        """
        Drives package collection based on the host operating system.
        
        Args:
            os_type: 'linux' or 'darwin'
            
        Returns:
            Dictionary with 'system_level' and 'language_runtimes' package lists
        """
        system_packages: List[str] = []
        runtime_packages: List[str] = []
        
        if os_type == "darwin":
            # Homebrew formulae
            brew_formulae = self.execute_command(["brew", "list", "--versions"])
            system_packages.extend(brew_formulae)
            
            # Homebrew casks
            brew_casks = self.execute_command(["brew", "list", "--casks", "--versions"])
            system_packages.extend(brew_casks)
            
        elif os_type == "linux":
            distro = self._get_linux_distro()
            
            if distro and distro in DISTRO_PACKAGE_MANAGERS:
                pm_args = DISTRO_PACKAGE_MANAGERS[distro]
                pm_output = self.execute_command(pm_args)
                system_packages.extend(pm_output)
            else:
                # Try each package manager in order
                for pm_name, pm_args in DISTRO_PACKAGE_MANAGERS.items():
                    pm_output = self.execute_command(pm_args)
                    if pm_output:
                        system_packages.extend(pm_output)
                        break
        
        # Global language runtimes (run on all platforms)
        
        # Node.js / npm
        npm_output = self.execute_command(["npm", "list", "-g", "--depth=0", "--parseable"])
        runtime_packages.extend([os.path.basename(p) for p in npm_output if p])
        
        # Python / pip
        pip_output = self.execute_command([sys.executable, "-m", "pip", "freeze"])
        runtime_packages.extend(pip_output)
        
        # Ruby / gem (optional, best effort)
        gem_output = self.execute_command(["gem", "list", "--local"])
        runtime_packages.extend(gem_output)
        
        # Rust / cargo (optional, best effort)
        cargo_output = self.execute_command(["cargo", "install", "--list"])
        runtime_packages.extend(cargo_output)
        
        return {
            "system_level": system_packages,
            "language_runtimes": runtime_packages
        }
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Collects basic system metadata.
        
        Returns:
            Dictionary with system metadata fields
        """
        raw_os = platform.system().lower()
        normalized_os = "linux" if raw_os == "linux" else ("darwin" if raw_os == "darwin" else "unknown")
        
        return {
            "os_platform": normalized_os,
            "kernel_version": platform.release(),
            "hostname": platform.node(),
            "architecture": platform.machine(),
        }
    
    def clear_errors(self) -> None:
        """Clear the error log."""
        self._errors = []
