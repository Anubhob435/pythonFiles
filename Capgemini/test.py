def filter_and_sort_logs(logs):
    """
    Filter logs by status (error/critical) and sort by date and time.
    
    Args:
        logs: List[List[str]] - 2D array with [date, time, status, message]
    
    Returns:
        List[List[str]] - Filtered and sorted logs
    """
    # Filter logs with status "error" or "critical"
    filtered_logs = [log for log in logs if log[2].lower() in ["error", "critical"]]
    
    # Function to convert date string to comparable format
    def date_to_comparable(date_str):

        day, month, year = date_str.split('-')
        return (int(year), int(month), int(day))
    
    # Function to convert time string to comparable format
    def time_to_comparable(time_str):

        hours, minutes = time_str.split(':')
        return (int(hours), int(minutes))
    
    # Sort by date first, then time (stable sort preserves original order for equal elements)
    filtered_logs.sort(key=lambda log: (date_to_comparable(log[0]), time_to_comparable(log[1])))
    
    return filtered_logs


# Example usage
if __name__ == "__main__":
    # Sample test data
    logs = [
        ["15-02-2026", "10:30", "info", "System started"],
        ["15-02-2026", "10:45", "error", "Connection failed"],
        ["14-02-2026", "23:15", "critical", "Database down"],
        ["15-02-2026", "10:45", "critical", "Out of memory"],
        ["16-02-2026", "08:00", "error", "Timeout occurred"],
        ["14-02-2026", "23:15", "error", "Auth failed"],
        ["15-02-2026", "09:30", "warning", "High CPU usage"]
    ]
    
    result = filter_and_sort_logs(logs)
    
    print("Filtered and Sorted Logs:")
    for log in result:
        print(log)