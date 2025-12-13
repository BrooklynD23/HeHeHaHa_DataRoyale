"""
System utilities for hardware detection and optimization.

Functions for detecting CUDA/GPU availability and configuring
machine learning frameworks to use available hardware acceleration.
"""

import os
import sys
import warnings
from typing import Dict, Any, Tuple


def safe_print(*args, **kwargs):
    """
    Print function that handles Unicode encoding errors gracefully.
    Falls back to ASCII if emojis can't be displayed (e.g., Windows console).
    """
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Fallback: replace emojis with ASCII equivalents
        text = ' '.join(str(arg) for arg in args)
        # Common emoji replacements
        replacements = {
            '🖥️': '[PC]',
            '✅': '[OK]',
            '❌': '[X]',
            '💻': '[CPU]',
            '🎮': '[GPU]',
            '📊': '[INFO]',
            '⚡': '[GPU]',
            '🔬': '[ML]',
            '💡': '[TIP]',
            '⚠️': '[WARN]',
            '🧵': '[THREAD]',
            '⚙️': '[CONFIG]',
            '📝': '[NOTE]',
        }
        for emoji, replacement in replacements.items():
            text = text.replace(emoji, replacement)
        print(text, **kwargs)


def check_cuda_availability() -> Dict[str, Any]:
    """
    Check if CUDA is available for GPU acceleration.

    Returns:
        dict: Information about CUDA availability with keys:
            - 'cuda_available': bool - Whether CUDA is available
            - 'device_count': int - Number of CUDA devices (0 if not available)
            - 'device_name': str or None - Name of primary GPU device
            - 'torch_available': bool - Whether PyTorch is installed
            - 'torch_cuda_built': bool - Whether PyTorch was built with CUDA support
            - 'torch_version': str or None - PyTorch version string
            - 'system_cuda_version': str or None - System CUDA version (from nvidia-smi)
            - 'xgboost_gpu': bool - Whether XGBoost can use GPU
            - 'sklearn_gpu': bool - Whether scikit-learn can use GPU (via cuML)
            - 'recommended_device': str - 'cuda' or 'cpu'
            - 'issue': str or None - Description of why GPU is not available

    Example:
        >>> cuda_info = check_cuda_availability()
        >>> if cuda_info['cuda_available']:
        ...     print(f"Found GPU: {cuda_info['device_name']}")
        ... else:
        ...     print("Running on CPU")
    """
    result = {
        'cuda_available': False,
        'device_count': 0,
        'device_name': None,
        'torch_available': False,
        'torch_cuda_built': False,
        'torch_version': None,
        'system_cuda_version': None,
        'xgboost_gpu': False,
        'sklearn_gpu': False,
        'recommended_device': 'cpu',
        'issue': None
    }

    # Check system CUDA version (via nvidia-smi)
    try:
        import subprocess
        nvidia_smi = subprocess.run(
            ['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'],
            capture_output=True, text=True, timeout=5
        )
        if nvidia_smi.returncode == 0:
            # Try to get CUDA version from nvidia-smi
            cuda_query = subprocess.run(
                ['nvidia-smi'], capture_output=True, text=True, timeout=5
            )
            if cuda_query.returncode == 0:
                # Extract CUDA version from output (e.g., "CUDA Version: 12.9")
                import re
                match = re.search(r'CUDA Version:\s*(\d+\.\d+)', cuda_query.stdout)
                if match:
                    result['system_cuda_version'] = match.group(1)
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        pass

    # Check PyTorch CUDA availability
    try:
        import torch
        result['torch_available'] = True
        result['torch_version'] = torch.__version__
        result['torch_cuda_built'] = torch.version.cuda is not None
        result['cuda_available'] = torch.cuda.is_available()

        if result['cuda_available']:
            result['device_count'] = torch.cuda.device_count()
            result['device_name'] = torch.cuda.get_device_name(0)
            result['recommended_device'] = 'cuda'
        else:
            # Determine why CUDA is not available
            if not result['torch_cuda_built']:
                result['issue'] = 'PyTorch CPU-only version installed (no CUDA support)'
            elif result['system_cuda_version']:
                result['issue'] = f'PyTorch built for CUDA but runtime not available (system CUDA: {result["system_cuda_version"]})'
            else:
                result['issue'] = 'CUDA runtime not available'
    except ImportError:
        result['issue'] = 'PyTorch not installed'

    # Check XGBoost GPU support
    try:
        import xgboost as xgb
        # XGBoost can use GPU if CUDA is available and it was compiled with GPU support
        result['xgboost_gpu'] = result['cuda_available']
    except ImportError:
        pass

    # Check cuML (GPU-accelerated scikit-learn alternative)
    try:
        import cuml
        result['sklearn_gpu'] = result['cuda_available']
    except ImportError:
        pass

    return result


def print_cuda_info(verbose: bool = True) -> None:
    """
    Print CUDA availability information in a human-readable format.

    Args:
        verbose: If True, print detailed information. If False, print summary only.

    Example:
        >>> print_cuda_info()
        🖥️  Hardware Detection:
        ✅ CUDA Available: Yes
        🎮 GPU Device: NVIDIA GeForce RTX 3080
        📊 Device Count: 1
        ⚡ XGBoost GPU: Enabled
        🔬 scikit-learn GPU: Not Available (install cuML for GPU support)
        💡 Recommended: Use 'cuda' for training
    """
    info = check_cuda_availability()

    safe_print("\n🖥️  Hardware Detection:")
    safe_print("=" * 60)

    if info['cuda_available']:
        safe_print("✅ CUDA Available: Yes")
        safe_print(f"🎮 GPU Device: {info['device_name']}")
        safe_print(f"📊 Device Count: {info['device_count']}")

        if info['xgboost_gpu']:
            safe_print("⚡ XGBoost GPU: Enabled")
        else:
            safe_print("⚠️  XGBoost GPU: Not Available (install GPU-enabled XGBoost)")

        if info['sklearn_gpu']:
            safe_print("🔬 scikit-learn GPU: Enabled (cuML)")
        else:
            safe_print("🔬 scikit-learn GPU: Not Available (install cuML for GPU support)")

        safe_print(f"💡 Recommended: Use '{info['recommended_device']}' for training")

        if verbose:
            safe_print("\n📝 GPU Memory Info:")
            try:
                import torch
                for i in range(info['device_count']):
                    total_mem = torch.cuda.get_device_properties(i).total_memory / 1e9
                    safe_print(f"   Device {i}: {total_mem:.2f} GB total memory")
            except:
                safe_print("   Unable to query GPU memory")
    else:
        safe_print("❌ CUDA Available: No")
        safe_print("💻 Running on: CPU")
        safe_print("💡 Recommended: Use 'cpu' for training")

        if verbose:
            safe_print("\n📝 To enable GPU acceleration:")
            cuda_info = check_cuda_availability()
            
            if cuda_info.get('system_cuda_version'):
                safe_print(f"   System CUDA version detected: {cuda_info['system_cuda_version']}")
            
            if cuda_info.get('issue') == 'PyTorch CPU-only version installed (no CUDA support)':
                safe_print("   ⚠️  Issue: PyTorch CPU-only version is installed")
                safe_print("   Solution: Install PyTorch with CUDA support")
                if cuda_info.get('system_cuda_version'):
                    cuda_major = cuda_info['system_cuda_version'].split('.')[0]
                    if cuda_major == '12':
                        safe_print("   For CUDA 12.x: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
                    elif cuda_major == '11':
                        safe_print("   For CUDA 11.8: pip install torch --index-url https://download.pytorch.org/whl/cu118")
                    else:
                        safe_print("   Check PyTorch website for your CUDA version: https://pytorch.org/get-started/locally/")
                else:
                    safe_print("   For CUDA 12.1: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
                    safe_print("   For CUDA 11.8: pip install torch --index-url https://download.pytorch.org/whl/cu118")
            else:
                safe_print("   1. Ensure NVIDIA GPU with CUDA support is available")
                safe_print("   2. Install CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
                safe_print("   3. Install PyTorch with CUDA: pip install torch --index-url https://download.pytorch.org/whl/cu121")
            
            safe_print("   4. Install XGBoost with GPU: pip install xgboost[gpu]")
            safe_print("   5. (Optional) Install cuML: pip install cuml-cu11")

    safe_print("=" * 60 + "\n")


def get_xgboost_params(use_gpu: bool = None, n_jobs: int = -1) -> Dict[str, Any]:
    """
    Get XGBoost parameters optimized for available hardware.

    Args:
        use_gpu: If True, force GPU. If False, force CPU. If None, auto-detect.
        n_jobs: Number of parallel threads for CPU (-1 = all cores)

    Returns:
        dict: XGBoost parameters optimized for hardware

    Example:
        >>> params = get_xgboost_params()
        >>> model = xgb.XGBClassifier(**params, n_estimators=100)
    """
    cuda_info = check_cuda_availability()

    # Auto-detect if not specified
    if use_gpu is None:
        use_gpu = cuda_info['xgboost_gpu']

    params = {
        'n_jobs': n_jobs,
        'random_state': 42,
    }

    if use_gpu and cuda_info['cuda_available']:
        params.update({
            'tree_method': 'gpu_hist',
            'gpu_id': 0,
            'predictor': 'gpu_predictor',
        })
        safe_print("⚡ XGBoost: Using GPU acceleration")
    else:
        params.update({
            'tree_method': 'hist',  # Fast CPU histogram-based algorithm
            'predictor': 'cpu_predictor',
        })
        safe_print("💻 XGBoost: Using CPU")

    return params


def get_sklearn_device() -> str:
    """
    Get recommended device for scikit-learn models.

    Returns:
        str: 'cuda' if GPU available, 'cpu' otherwise

    Note:
        Standard scikit-learn doesn't support GPU. This function is for
        future compatibility with cuML (GPU-accelerated scikit-learn).
    """
    cuda_info = check_cuda_availability()
    return cuda_info['recommended_device']


def optimize_duckdb_threads(max_threads: int = None) -> int:
    """
    Get optimal thread count for DuckDB based on available CPU cores.

    Args:
        max_threads: Maximum threads to use. If None, use all available cores.

    Returns:
        int: Recommended thread count

    Example:
        >>> con = duckdb.connect()
        >>> threads = optimize_duckdb_threads()
        >>> con.execute(f"SET threads TO {threads}")
    """
    try:
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
    except:
        cpu_count = 4  # Fallback

    if max_threads is None:
        # Use all cores for DuckDB (it's memory-bound, not CPU-bound)
        return cpu_count
    else:
        return min(cpu_count, max_threads)


def configure_environment_for_ml(verbose: bool = True) -> Dict[str, Any]:
    """
    Configure environment variables and settings for optimal ML performance.

    Args:
        verbose: If True, print configuration details

    Returns:
        dict: Configuration summary

    Example:
        >>> config = configure_environment_for_ml()
        >>> # Environment is now optimized
    """
    cuda_info = check_cuda_availability()

    config = {
        'cuda_available': cuda_info['cuda_available'],
        'duckdb_threads': optimize_duckdb_threads(),
        'xgboost_device': 'gpu' if cuda_info['xgboost_gpu'] else 'cpu',
        'sklearn_device': get_sklearn_device()
    }

    # Set environment variables for optimal performance
    if cuda_info['cuda_available']:
        # Optimize CUDA settings
        os.environ['CUDA_LAUNCH_BLOCKING'] = '0'  # Async CUDA operations
        os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'  # Don't hog all GPU memory
    else:
        # Optimize CPU settings
        os.environ['OMP_NUM_THREADS'] = str(config['duckdb_threads'])
        os.environ['MKL_NUM_THREADS'] = str(config['duckdb_threads'])

    if verbose:
        safe_print("\n⚙️  Environment Configuration:")
        safe_print("=" * 60)
        safe_print(f"🖥️  Device: {'GPU (CUDA)' if config['cuda_available'] else 'CPU'}")
        safe_print(f"🧵 DuckDB Threads: {config['duckdb_threads']}")
        safe_print(f"⚡ XGBoost: {config['xgboost_device'].upper()}")
        safe_print(f"🔬 scikit-learn: {config['sklearn_device'].upper()}")
        safe_print("=" * 60 + "\n")

    return config


def get_memory_info() -> Dict[str, float]:
    """
    Get system memory information.

    Returns:
        dict: Memory info with keys 'total_gb', 'available_gb', 'percent_used'
    """
    try:
        import psutil
        mem = psutil.virtual_memory()
        return {
            'total_gb': mem.total / 1e9,
            'available_gb': mem.available / 1e9,
            'percent_used': mem.percent
        }
    except ImportError:
        warnings.warn("psutil not installed. Cannot get memory info.")
        return {
            'total_gb': None,
            'available_gb': None,
            'percent_used': None
        }


# Auto-detect on module import (can be disabled by setting env var)
if os.environ.get('SKIP_CUDA_CHECK', '0') == '0':
    _cuda_info = check_cuda_availability()
    if _cuda_info['cuda_available']:
        safe_print(f"✅ GPU Detected: {_cuda_info['device_name']}")
    else:
        safe_print("💻 Running on CPU (no GPU detected)")
