#!/usr/bin/env python3
import os
import sys
import urllib.request
import time
import tarfile

def download_with_progress(url, destination):
    """
    Downloads a file with a progress bar
    """
    print(f"Downloading {url} to {destination}")
    
    def report_progress(block_num, block_size, total_size):
        # Calculate progress percentage
        downloaded = block_num * block_size
        percent = min(100, downloaded * 100 / total_size)
        
        # Calculate download speed
        current_time = time.time()
        if 'start_time' not in report_progress.__dict__:
            report_progress.start_time = current_time
            report_progress.last_time = current_time
            report_progress.last_downloaded = 0
        
        if current_time - report_progress.last_time >= 1:  # Update every second
            speed = (downloaded - report_progress.last_downloaded) / (current_time - report_progress.last_time)
            report_progress.last_time = current_time
            report_progress.last_downloaded = downloaded
            
            # Convert to appropriate unit
            if speed < 1024:
                speed_str = f"{speed:.2f} B/s"
            elif speed < 1024 * 1024:
                speed_str = f"{speed / 1024:.2f} KB/s"
            else:
                speed_str = f"{speed / (1024 * 1024):.2f} MB/s"
                
            # Calculate estimated time remaining
            elapsed = current_time - report_progress.start_time
            if downloaded > 0:
                estimated_total = (total_size / downloaded) * elapsed
                remaining = estimated_total - elapsed
                time_str = f"ETA: {int(remaining / 60)}m {int(remaining % 60)}s"
            else:
                time_str = "ETA: calculating..."
                
            # Convert downloaded to appropriate unit
            if total_size < 1024 * 1024:
                size_str = f"{downloaded / 1024:.2f} KB / {total_size / 1024:.2f} KB"
            else:
                size_str = f"{downloaded / (1024 * 1024):.2f} MB / {total_size / (1024 * 1024):.2f} MB"
            
            # Print progress
            sys.stdout.write(f"\r{percent:.1f}% | {size_str} | {speed_str} | {time_str}")
            sys.stdout.flush()
    
    try:
        urllib.request.urlretrieve(url, destination, reporthook=report_progress)
        print("\nDownload completed successfully!")
        return True
    except Exception as e:
        print(f"\nError downloading file: {e}")
        return False

def extract_tarfile(filename, extract_dir):
    """
    Extracts a tar file to the specified directory
    """
    try:
        print(f"Extracting {filename} to {extract_dir}...")
        with tarfile.open(filename) as tar:
            tar.extractall(path=extract_dir)
        print("Extraction completed successfully!")
        return True
    except Exception as e:
        print(f"Error extracting file: {e}")
        return False

def main():
    # URL for the Ubuntu Dialogue Corpus
    url = "http://cs.mcgill.ca/~jpineau/datasets/ubuntu-corpus-1.0/ubuntu_dialogs.tgz"
    
    # Destination filename
    destination = "ubuntu_dialogs.tgz"
    
    # Extract directory
    extract_dir = "."
    
    # Download the file
    if not os.path.exists(destination):
        success = download_with_progress(url, destination)
        if not success:
            print("Download failed. Please try again.")
            return
    else:
        print(f"File {destination} already exists. Skipping download.")
    
    # Ask user if they want to extract the file
    extract = input("Do you want to extract the file? (y/n): ").lower()
    if extract == 'y':
        extract_tarfile(destination, extract_dir)
    
if __name__ == "__main__":
    main() 