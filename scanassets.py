@api_router.get("/scans/{scan_id}/export")
async def export_scan_assets_csv(scan_id: str):
    """Export assets discovered in a specific scan to CSV format"""
    # Get scan details
    scan = await db.scan_results.find_one({"id": scan_id})
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Get assets from this scan
    assets = await db.assets.find({"scan_id": scan_id}).to_list(length=None)
    
    # Create CSV content
    output = io.StringIO()
    fieldnames = [
        'scan_id', 'ip_address', 'hostname', 'mac_address', 'os_type', 'os_version',
        'asset_type', 'status', 'role', 'environment', 'cloud_provider', 'cloud_region',
        'ports_open', 'services', 'tags', 'last_seen', 'first_discovered'
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for asset in assets:
        row = {
            'scan_id': asset.get('scan_id', ''),
            'ip_address': asset.get('ip_address', ''),
            'hostname': asset.get('hostname', ''),
            'mac_address': asset.get('mac_address', ''),
            'os_type': asset.get('os_type', ''),
            'os_version': asset.get('os_version', ''),
            'asset_type': asset.get('asset_type', ''),
            'status': asset.get('status', ''),
            'role': asset.get('role', ''),
            'environment': asset.get('environment', ''),
            'cloud_provider': asset.get('cloud_provider', ''),
            'cloud_region': asset.get('cloud_region', ''),
            'ports_open': ','.join(map(str, asset.get('ports_open', []))),
            'services': ','.join(asset.get('services', [])),
            'tags': ','.join(asset.get('tags', [])),
            'last_seen': asset.get('last_seen', ''),
            'first_discovered': asset.get('first_discovered', '')
        }
        writer.writerow(row)
    
    csv_content = output.getvalue()
    output.close()
    
    # Get scan name from config if available
    scan_config = await db.scan_configs.find_one({"id": scan.get('scan_config_id')})
    scan_name = scan_config.get('name', 'Unknown') if scan_config else 'Unknown'
    
    return {
        "filename": f"scan_{scan_name.replace(' ', '_')}_{scan_id[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        "content": csv_content,
        "count": len(assets),
        "scan_name": scan_name,
        "scan_status": scan.get('status'),
        "scan_start_time": scan.get('start_time')
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
