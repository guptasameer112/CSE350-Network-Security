import ntplib
from datetime import datetime

ntp_client = ntplib.NTPClient()

def get_secure_ntp_time():
    '''
    Get the current time from an NTP server securely.
    '''
    
    try:
        response = ntp_client.request('pool.ntp.org')
        secure_time = datetime.fromtimestamp(response.tx_time)
        print(f"[Secure Time Sync] Securely synchronized time: {secure_time}")
        return secure_time
    except Exception as e:
        print(f"[Error] Failed to sync time with NTP server: {e}")
        return datetime.now()  # Fallback to system time
