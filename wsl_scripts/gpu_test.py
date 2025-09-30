#!/usr/bin/env python3
"""
Comprehensive TensorFlow setup check for WSL + GPU
"""

import sys
import tensorflow as tf

def check_tensorflow_setup():
    print("=" * 50)
    print("TensorFlow Setup Check")
    print("=" * 50)
    
    # Basic info
    print(f"Python version: {sys.version}")
    print(f"TensorFlow version: {tf.__version__}")
    print()
    
    # CUDA support
    print("CUDA Support:")
    print(f"  Built with CUDA: {tf.test.is_built_with_cuda()}")
    print(f"  CUDA runtime version: {tf.sysconfig.get_build_info().get('cuda_version', 'Not available')}")
    print()
    
    # GPU devices
    print("GPU Devices:")
    gpus = tf.config.list_physical_devices('GPU')
    print(f"  Number of GPUs: {len(gpus)}")
    
    if gpus:
        for i, gpu in enumerate(gpus):
            print(f"  GPU {i}: {gpu}")
            
        # Test GPU computation
        print("\nTesting GPU computation...")
        try:
            with tf.device('/GPU:0'):
                # Create some test tensors
                a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
                b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
                c = tf.matmul(a, b)
                print(f"  GPU computation successful!")
                print(f"  Result shape: {c.shape}")
                print(f"  Result: {c.numpy()}")
                return True
        except Exception as e:
            print(f"  GPU computation failed: {e}")
            return False
    else:
        print("  No GPUs found. TensorFlow will use CPU.")
        return False

if __name__ == "__main__":
    success = check_tensorflow_setup()
    print("\n" + "=" * 50)
    if success:
        print("✅ TensorFlow GPU setup is working correctly!")
    else:
        print("❌ TensorFlow GPU setup needs attention.")
    print("=" * 50)
