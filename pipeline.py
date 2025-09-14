#!/usr/bin/env python3
"""
Complete Industrial Process Monitoring Pipeline
This script orchestrates the full workflow:
1. Generate synthetic data (CSV files)
2. Create visualization plots from the generated data
3. Analyze the plots using AI vision model for anomaly detection
"""

import time
import subprocess
import sys
import os
import shutil
from datetime import datetime
from pathlib import Path

# Import our modules
from synth_data import generate_and_save_data
from plot_data import create_dashboard

def run_plot_analysis():
    """Run the AI-powered plot analysis"""
    try:
        print("🤖 Running AI analysis of the generated plot...")
        
        # Import the analysis modules here to avoid loading the model unless needed
        from mlx_vlm import load, generate
        from mlx_vlm.prompt_utils import apply_chat_template
        from mlx_vlm.utils import load_config
        
        model_path = "mlx-community/LFM2-VL-450M-8bit"
        print(f"📥 Loading model: {model_path}")
        model, processor = load(model_path, trust_remote_code=True)
        config = model.config
        
        images = ["images/culprit_signals_analysis.png"]
        prompt = """Detect and rank sensors that show anomalous readings or patterns compared to normal operational ranges in the Waste Heat Recovery System datasets. Focus on statistical outliers, sudden spikes or drops, and values that correlate with event alerts or warnings. Highlight the sensors most likely responsible for process deviations or abnormal events."""
        
        formatted_prompt = apply_chat_template(
            processor, config, prompt, num_images=len(images)
        )
        
        print("🔍 Analyzing plot for anomalies...")
        output = generate(model, processor, formatted_prompt, images, verbose=False)
        
        return output
        
    except ImportError as e:
        print(f"❌ Error importing MLX VLM modules: {e}")
        print("Make sure mlx-vlm is installed: pip install mlx-vlm")
        return None
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return None

def run_complete_pipeline():
    """Run the complete pipeline: data generation -> plotting -> analysis"""
    print("=" * 80)
    print("🏭 COMPLETE INDUSTRIAL PROCESS MONITORING PIPELINE")
    print("=" * 80)
    print(f"Pipeline started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Generate synthetic data
    print("STEP 1: Generating synthetic data...")
    print("-" * 50)
    try:
        generate_and_save_data()
        print("✅ Data generation completed successfully")
    except Exception as e:
        print(f"❌ Error in data generation: {e}")
        return False
    print()
    
    # Step 2: Create visualization
    print("STEP 2: Creating visualization...")
    print("-" * 50)
    try:
        create_dashboard()
        print("✅ Visualization created successfully")
    except Exception as e:
        print(f"❌ Error in visualization: {e}")
        return False
    print()
    
    # Step 3: AI Analysis
    print("STEP 3: AI-Powered Anomaly Analysis...")
    print("-" * 50)
    analysis_result = run_plot_analysis()
    
    if analysis_result:
        print("✅ AI Analysis completed successfully")
        
        # Save analysis to analysis folder with archiving
        save_analysis_report(analysis_result, save_to_analysis_folder=True)
        
        print()
        print("🔍 ANALYSIS RESULTS:")
        print("=" * 50)
        analysis_text = analysis_result.text if hasattr(analysis_result, 'text') else str(analysis_result)
        print(analysis_text)
        print("=" * 50)
    else:
        print("❌ AI Analysis failed or skipped")
    print()
    
    print("=" * 80)
    print(f"Pipeline completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return True

def run_continuous_pipeline(interval_seconds=60):
    """Run continuous pipeline cycles"""
    print("=" * 80)
    print("🔄 CONTINUOUS INDUSTRIAL PROCESS MONITORING PIPELINE")
    print("=" * 80)
    print(f"Running continuous pipeline every {interval_seconds} seconds")
    print("Press Ctrl+C to stop")
    print()
    
    cycle_count = 0
    
    try:
        while True:
            cycle_count += 1
            print(f"\n🔄 PIPELINE CYCLE #{cycle_count}")
            print("=" * 60)
            
            # Step 1: Generate synthetic data
            print("📊 Generating synthetic data...")
            try:
                generate_and_save_data()
            except Exception as e:
                print(f"❌ Data generation error: {e}")
                continue
            
            # Step 2: Create visualization
            print("📈 Creating visualization...")
            try:
                create_dashboard()
            except Exception as e:
                print(f"❌ Visualization error: {e}")
                continue
            
            # Step 3: AI Analysis
            print("🤖 Running AI analysis...")
            analysis_result = run_plot_analysis()
            
            if analysis_result:
                # Save analysis to analysis folder with archiving
                save_analysis_report(analysis_result, save_to_analysis_folder=True)
                
                print(f"✅ Cycle #{cycle_count} completed with analysis at {datetime.now().strftime('%H:%M:%S')}")
                print("📋 Latest Analysis Summary:")
                # Show first 200 characters of analysis text
                analysis_text = analysis_result.text if hasattr(analysis_result, 'text') else str(analysis_result)
                summary = analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text
                print(f"   {summary}")
            else:
                print(f"⚠️  Cycle #{cycle_count} completed (analysis failed) at {datetime.now().strftime('%H:%M:%S')}")
            
            print(f"⏳ Waiting {interval_seconds} seconds for next cycle...")
            
            # Wait for next cycle
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Pipeline stopped after {cycle_count} cycles")
        print("Final files available:")
        print("- data/events.csv")
        print("- data/sensors.csv") 
        print("- images/culprit_signals_analysis.png")
        print("- analysis/analysis_report.txt")

def archive_existing_analysis():
    """Archive existing analysis file with timestamp"""
    analysis_dir = "analysis"
    archive_dir = "analysis/archive"
    
    # Ensure directories exist
    os.makedirs(analysis_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Archive existing analysis if it exists
    filename = "analysis_report.txt"
    filepath = os.path.join(analysis_dir, filename)
    if os.path.exists(filepath):
        # Create archived filename with timestamp
        name, ext = os.path.splitext(filename)
        archived_filename = f"{name}_{timestamp}{ext}"
        archived_filepath = os.path.join(archive_dir, archived_filename)
        
        # Move file to archive
        shutil.move(filepath, archived_filepath)
        print(f"Archived {filename} to {archived_filename}")

def save_analysis_report(analysis_result, save_to_analysis_folder=True):
    """Save the analysis result to analysis folder with archiving"""
    if not analysis_result:
        return
    
    # Extract text from GenerationResult object
    analysis_text = analysis_result.text if hasattr(analysis_result, 'text') else str(analysis_result)
    
    if save_to_analysis_folder:
        # Archive existing analysis first
        archive_existing_analysis()
        
        # Save to analysis folder
        analysis_dir = "analysis"
        os.makedirs(analysis_dir, exist_ok=True)
        report_filename = os.path.join(analysis_dir, "analysis_report.txt")
        location_msg = "analysis/analysis_report.txt"
    else:
        # Save to root with timestamp (legacy mode)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"analysis_report_{timestamp}.txt"
        location_msg = report_filename
    
    try:
        with open(report_filename, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("INDUSTRIAL PROCESS MONITORING - ANOMALY ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Source plot: images/culprit_signals_analysis.png\n")
            f.write("=" * 80 + "\n\n")
            f.write(analysis_text)
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("End of Report\n")
        
        print(f"📄 Analysis report saved to: {location_msg}")
        return report_filename
    except Exception as e:
        print(f"❌ Error saving report: {e}")
        return None

def main():
    """Main function to choose pipeline mode"""
    print("🏭 Industrial Process Monitoring Pipeline")
    print("Choose pipeline mode:")
    print("1. Single pipeline run (generate data + plot + analyze)")
    print("2. Single pipeline run + save report")
    print("3. Continuous pipeline (every 60 seconds)")
    print("4. Custom interval continuous pipeline")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_complete_pipeline()
            
        elif choice == "2":
            success = run_complete_pipeline()
            if success:
                print("📄 Analysis report already saved to analysis folder during pipeline execution")
            
        elif choice == "3":
            run_continuous_pipeline(60)
            
        elif choice == "4":
            try:
                interval = int(input("Enter interval in seconds (minimum 30): "))
                if interval < 30:
                    print("Minimum interval is 30 seconds. Setting to 30 seconds.")
                    interval = 30
                run_continuous_pipeline(interval)
            except ValueError:
                print("Invalid interval. Using default 60 seconds.")
                run_continuous_pipeline(60)
                
        else:
            print("Invalid choice. Running single pipeline.")
            run_complete_pipeline()
            
    except KeyboardInterrupt:
        print("\n\nPipeline cancelled by user.")

if __name__ == "__main__":
    main()