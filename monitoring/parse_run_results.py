import json
import yaml
from pathlib import Path
from datetime import datetime

def parse_dbt_run_results(results_path: str = "target/run_results.json"):
    """
    Parse dbt run_results.json to extract execution metrics and generate quality reports.
    
    Args:
        results_path: Path to dbt run_results.json file
        
    Returns:
        dict: Parsed metrics and quality indicators
    """
    try:
        with open(results_path, 'r') as f:
            run_results = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {results_path}")
        return None
    
    # Extract metrics
    metrics = {
        'timestamp': datetime.now().isoformat(),
        'total_nodes': len(run_results.get('results', [])),
        'successful_nodes': sum(1 for r in run_results.get('results', []) if r['status'] == 'success'),
        'failed_nodes': sum(1 for r in run_results.get('results', []) if r['status'] == 'error'),
        'skipped_nodes': sum(1 for r in run_results.get('results', []) if r['status'] == 'skipped'),
        'execution_time': run_results.get('elapsed_time', 0),
    }
    
    # Calculate quality indicators
    total = metrics['total_nodes']
    if total > 0:
        metrics['success_rate'] = metrics['successful_nodes'] / total
        metrics['error_rate'] = metrics['failed_nodes'] / total
    
    return metrics

def generate_quality_report(metrics: dict, output_path: str = "monitoring/quality_report.yaml"):
    """
    Generate a quality report based on parsed metrics.
    
    Args:
        metrics: Dictionary of parsed metrics
        output_path: Output path for the report
    """
    if metrics is None:
        return
    
    report = {
        'report_generated_at': metrics['timestamp'],
        'summary': {
            'total_nodes': metrics['total_nodes'],
            'successful': metrics['successful_nodes'],
            'failed': metrics['failed_nodes'],
            'skipped': metrics['skipped_nodes'],
        },
        'quality_metrics': {
            'success_rate': f"{metrics.get('success_rate', 0):.2%}",
            'error_rate': f"{metrics.get('error_rate', 0):.2%}",
            'execution_time_seconds': metrics['execution_time'],
        }
    }
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        yaml.dump(report, f, default_flow_style=False)
    
    print(f"Quality report saved to {output_path}")

if __name__ == "__main__":
    metrics = parse_dbt_run_results()
    if metrics:
        print(json.dumps(metrics, indent=2))
        generate_quality_report(metrics)
