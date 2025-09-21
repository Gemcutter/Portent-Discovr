@api_router.get("/scans/export")
async def export_scans_csv():
    """Export scan history to CSV format"""
    scans = await db.scan_results.find().sort("start_time", -1).to_list(length=None)
    
    # Create CSV content for scan history
    output = io.StringIO()
    fieldnames = [
        'scan_id', 'scan_config_id', 'status', 'progress', 'assets_discovered',
        'start_time', 'end_time', 'duration_seconds', 'error_message', 
        'total_assets', 'servers', 'endpoints', 'cloud_vms', 'network_devices', 'online', 'offline'
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for scan in scans:
       # Calculate duration
        duration_seconds = None
        if scan.get('end_time') and scan.get('start_time'):
            try:
                if isinstance(scan['end_time'], str):
                    end_time = datetime.fromisoformat(scan['end_time'].replace('Z', '+00:00'))
                else:
                    end_time = scan['end_time']
                
                if isinstance(scan['start_time'], str):
                    start_time = datetime.fromisoformat(scan['start_time'].replace('Z', '+00:00'))
                else:
                    start_time = scan['start_time']
                
                duration_seconds = int((end_time - start_time).total_seconds())
            except:
                duration_seconds = None
        
        # Extract summary data - ensure it's never None
        summary = scan.get('summary') or {}
        
        row = {
            'scan_id': scan.get('id', ''),
            'scan_config_id': scan.get('scan_config_id', ''),
            'status': scan.get('status', ''),
            'progress': scan.get('progress', 0),
            'assets_discovered': scan.get('assets_discovered', 0),
            'start_time': scan.get('start_time', ''),
            'end_time': scan.get('end_time', ''),
            'duration_seconds': duration_seconds,
            'error_message': scan.get('error_message', ''),
            'total_assets': summary.get('total_assets', ''),
            'servers': summary.get('servers', ''),
            'endpoints': summary.get('endpoints', ''),
            'cloud_vms': summary.get('cloud_vms', ''),
            'network_devices': summary.get('network_devices', ''),
            'online': summary.get('online', ''),
            'offline': summary.get('offline', '')
        }
        writer.writerow(row)
    
    csv_content = output.getvalue()
    output.close()
    
    return {
        "filename": f"scan_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        "content": csv_content,
        "count": len(scans)

