#!/usr/bin/env python3

import os
import sys
import time
import signal
import subprocess
import psutil

def find_running_instances():
    """Find any running instances of yap_gui.py"""
    running_instances = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any('yap_gui.py' in arg for arg in cmdline if arg):
                running_instances.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return running_instances

def close_instances(instances):
    """Gracefully close running instances"""
    if not instances:
        print("✅ No running instances found")
        return
    
    print(f"⚠️  Found {len(instances)} running instance(s)")
    print("🔄 Closing existing instance(s)...")
    
    for proc in instances:
        try:
            print(f"   Stopping process {proc.pid}...")
            
            # Try graceful termination first
            proc.terminate()
            
            # Wait for graceful shutdown
            try:
                proc.wait(timeout=3)
                print(f"   ✅ Process {proc.pid} closed gracefully")
            except psutil.TimeoutExpired:
                # Force kill if still running
                print(f"   ⚡ Force stopping process {proc.pid}...")
                proc.kill()
                proc.wait()
                print(f"   ✅ Process {proc.pid} force closed")
                
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"   ⚠️  Could not close process {proc.pid}: {e}")
    
    print("✅ Existing instances closed")
    time.sleep(2)

def main():
    """Main launcher function"""
    print("🔍 Checking for running Whisper Killer instances...")
    
    # Find running instances
    running_instances = find_running_instances()
    
    # Close existing instances
    close_instances(running_instances)
    
    print("🚀 Starting Whisper Killer...")
    print("")
    
    try:
        # Start the application
        result = subprocess.run([sys.executable, 'yap_gui.py'], 
                              cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print("")
            print("✅ Whisper Killer started successfully")
        else:
            print("")
            print(f"❌ Whisper Killer exited with code {result.returncode}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("")
        print("🛑 Whisper Killer stopped by user")
    except Exception as e:
        print("")
        print(f"❌ Failed to start Whisper Killer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 