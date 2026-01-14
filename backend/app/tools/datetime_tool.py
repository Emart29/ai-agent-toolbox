"""
DateTime Tool
Get current time, dates, and perform date/time calculations

Features:
- Current time in any timezone
- Date calculations (add/subtract days, weeks, months)
- Time difference calculations
- Format conversions
- Timezone conversions
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DateTimeTool:
    """
    DateTime tool for time and date operations.
    
    Handles timezone conversions, date arithmetic, and formatting.
    """
    
    def __init__(self):
        """Initialize datetime tool"""
        # Common timezones
        self.common_timezones = {
            'UTC': 'UTC',
            'GMT': 'GMT',
            'EST': 'US/Eastern',
            'PST': 'US/Pacific',
            'CST': 'US/Central',
            'MST': 'US/Mountain',
            'WAT': 'Africa/Lagos',  # West Africa Time (Nigeria)
            'CET': 'Europe/Paris',
            'JST': 'Asia/Tokyo',
            'IST': 'Asia/Kolkata',
            'AEST': 'Australia/Sydney',
        }
        
        logger.info("DateTimeTool initialized")
    
    def get_current_time(self, timezone: Optional[str] = None, format_str: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current time.
        
        Args:
            timezone: Timezone name (e.g., 'UTC', 'US/Eastern', 'Africa/Lagos')
            format_str: Custom format string (e.g., '%Y-%m-%d %H:%M:%S')
            
        Returns:
            Dict with current time information
        """
        try:
            # Get timezone
            if timezone:
                # Check if it's a common timezone abbreviation
                tz_name = self.common_timezones.get(timezone.upper(), timezone)
                tz = pytz.timezone(tz_name)
            else:
                tz = pytz.UTC
            
            # Get current time
            now = datetime.now(tz)
            
            # Format output
            if format_str:
                formatted_time = now.strftime(format_str)
            else:
                formatted_time = now.strftime('%Y-%m-%d %H:%M:%S %Z')
            
            return {
                'success': True,
                'datetime': formatted_time,
                'timezone': str(tz),
                'timestamp': now.timestamp(),
                'iso_format': now.isoformat(),
                'explanation': f"Current time in {tz}: {formatted_time}"
            }
            
        except Exception as e:
            logger.error(f"Error getting current time: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': f'Failed to get current time for timezone: {timezone}'
            }
    
    def add_time(self, base_time: Optional[str], days: int = 0, hours: int = 0, 
                 minutes: int = 0, weeks: int = 0) -> Dict[str, Any]:
        """
        Add time to a date.
        
        Args:
            base_time: Starting datetime (ISO format) or None for current time
            days: Days to add
            hours: Hours to add
            minutes: Minutes to add
            weeks: Weeks to add
            
        Returns:
            Dict with calculated datetime
        """
        try:
            # Parse base time or use current
            if base_time:
                dt = datetime.fromisoformat(base_time)
            else:
                dt = datetime.now()
            
            # Add time
            result_dt = dt + timedelta(days=days, hours=hours, minutes=minutes, weeks=weeks)
            
            # Calculate difference for explanation
            diff = result_dt - dt
            
            return {
                'success': True,
                'original_time': dt.isoformat(),
                'result_time': result_dt.isoformat(),
                'formatted_result': result_dt.strftime('%Y-%m-%d %H:%M:%S'),
                'difference_days': diff.days,
                'explanation': f"Starting from {dt.strftime('%Y-%m-%d %H:%M:%S')}, "
                              f"adding {weeks} weeks, {days} days, {hours} hours, {minutes} minutes "
                              f"gives: {result_dt.strftime('%Y-%m-%d %H:%M:%S')}"
            }
            
        except Exception as e:
            logger.error(f"Error adding time: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': 'Failed to calculate time addition'
            }
    
    def time_until(self, target_date: str, from_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate time until a target date.
        
        Args:
            target_date: Target date (ISO format or common formats)
            from_date: Starting date (default: now)
            
        Returns:
            Dict with time difference
        """
        try:
            # Parse dates
            target_dt = self._parse_date(target_date)
            
            if from_date:
                start_dt = self._parse_date(from_date)
            else:
                start_dt = datetime.now()
            
            # Calculate difference
            diff = target_dt - start_dt
            
            # Break down into components
            days = diff.days
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60
            
            # Build explanation
            if diff.days < 0:
                explanation = f"The target date {target_dt.strftime('%Y-%m-%d')} has already passed"
            elif diff.days == 0:
                explanation = f"Today! In {hours} hours and {minutes} minutes"
            elif diff.days == 1:
                explanation = f"Tomorrow ({days} day, {hours} hours)"
            else:
                weeks = days // 7
                remaining_days = days % 7
                
                if weeks > 0:
                    explanation = f"In {weeks} weeks and {remaining_days} days ({days} total days)"
                else:
                    explanation = f"In {days} days"
            
            return {
                'success': True,
                'from_date': start_dt.strftime('%Y-%m-%d'),
                'target_date': target_dt.strftime('%Y-%m-%d'),
                'days_difference': days,
                'hours_difference': days * 24 + hours,
                'total_seconds': diff.total_seconds(),
                'explanation': explanation
            }
            
        except Exception as e:
            logger.error(f"Error calculating time until: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': f'Failed to calculate time until: {target_date}'
            }
    
    def convert_timezone(self, time_str: str, from_tz: str, to_tz: str) -> Dict[str, Any]:
        """
        Convert time between timezones.
        
        Args:
            time_str: Time string (ISO format or common formats)
            from_tz: Source timezone
            to_tz: Target timezone
            
        Returns:
            Dict with converted time
        """
        try:
            # Parse timezones
            from_tz_name = self.common_timezones.get(from_tz.upper(), from_tz)
            to_tz_name = self.common_timezones.get(to_tz.upper(), to_tz)
            
            from_timezone = pytz.timezone(from_tz_name)
            to_timezone = pytz.timezone(to_tz_name)
            
            # Parse time
            dt = self._parse_date(time_str)
            
            # Localize to source timezone
            dt_localized = from_timezone.localize(dt)
            
            # Convert to target timezone
            dt_converted = dt_localized.astimezone(to_timezone)
            
            return {
                'success': True,
                'original_time': dt_localized.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'converted_time': dt_converted.strftime('%Y-%m-%d %H:%M:%S %Z'),
                'from_timezone': from_tz_name,
                'to_timezone': to_tz_name,
                'explanation': f"{dt_localized.strftime('%H:%M %Z')} is "
                              f"{dt_converted.strftime('%H:%M %Z')}"
            }
            
        except Exception as e:
            logger.error(f"Error converting timezone: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'explanation': f'Failed to convert timezone from {from_tz} to {to_tz}'
            }
    
    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse date string flexibly.
        
        Handles various date formats.
        """
        # Try ISO format first
        try:
            return datetime.fromisoformat(date_str)
        except:
            pass
        
        # Try common formats
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except:
                continue
        
        raise ValueError(f"Could not parse date: {date_str}")


# LangChain Tool wrapper
def get_datetime_tool_for_langchain():
    """
    Create LangChain-compatible datetime tool.
    """
    datetime_tool = DateTimeTool()
    
    def datetime_wrapper(action: str, **kwargs) -> str:
        """
        Perform datetime operations.
        
        Args:
            action: Action to perform (current_time, add_time, time_until, convert_timezone)
            **kwargs: Arguments for the action
            
        Returns:
            Result as string
        """
        action = action.lower()
        
        if action == 'current_time':
            result = datetime_tool.get_current_time(
                kwargs.get('timezone'),
                kwargs.get('format')
            )
        elif action == 'add_time':
            result = datetime_tool.add_time(
                kwargs.get('base_time'),
                kwargs.get('days', 0),
                kwargs.get('hours', 0),
                kwargs.get('minutes', 0),
                kwargs.get('weeks', 0)
            )
        elif action == 'time_until':
            result = datetime_tool.time_until(
                kwargs.get('target_date'),
                kwargs.get('from_date')
            )
        elif action == 'convert_timezone':
            result = datetime_tool.convert_timezone(
                kwargs.get('time'),
                kwargs.get('from_tz'),
                kwargs.get('to_tz')
            )
        else:
            result = {
                'success': False,
                'explanation': f'Unknown action: {action}'
            }
        
        return result['explanation']
    
    return datetime_wrapper


# Example usage and testing
if __name__ == "__main__":
    dt_tool = DateTimeTool()
    
    print("🧪 Testing DateTime Tool\n")
    
    # Test 1: Current time
    print("1️⃣ Current time (UTC):")
    result = dt_tool.get_current_time('UTC')
    print(f"   {result['explanation']}\n")
    
    # Test 2: Current time in Lagos
    print("2️⃣ Current time in Lagos:")
    result = dt_tool.get_current_time('Africa/Lagos')
    print(f"   {result['explanation']}\n")
    
    # Test 3: Add time
    print("3️⃣ Add 7 days:")
    result = dt_tool.add_time(None, days=7)
    print(f"   {result['explanation']}\n")
    
    # Test 4: Time until
    print("4️⃣ Time until New Year 2026:")
    result = dt_tool.time_until('2026-01-01')
    print(f"   {result['explanation']}\n")
    
    # Test 5: Timezone conversion
    print("5️⃣ Convert 2PM Lagos time to New York:")
    result = dt_tool.convert_timezone('2024-01-15 14:00:00', 'Africa/Lagos', 'US/Eastern')
    print(f"   {result['explanation']}\n")
    
    print("✅ All tests completed!")