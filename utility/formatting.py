def seconds_to_formatted_time(seconds):
        """
        Converts a given number of seconds into a formatted string showing either minutes or hours and minutes (if applicable).

        Parameters:
        seconds (int): The number of seconds to convert.

        Returns:
        str: A formatted string representing the time in minutes or hours and minutes.
        """
        formatted_time = ""

        minutes = seconds // 60
        hours = minutes // 60

        if seconds == 0:
            formatted_time = "0m"
        elif seconds < 60:
            formatted_time = f"{seconds}s"

        if hours > 0:
            formatted_time += f"{hours}h "
            minutes -= hours * 60

        if minutes > 0:
            formatted_time += f"{minutes}m "
            if seconds % 60 > 0:
                formatted_time += f"{seconds % 60}s"

        return formatted_time

if __name__ == '__main__':
     # Test extensively
        print(seconds_to_formatted_time(0))
        print(seconds_to_formatted_time(1))
        print(seconds_to_formatted_time(59))
        print(seconds_to_formatted_time(60))
        print(seconds_to_formatted_time(61))
        print(seconds_to_formatted_time(119))
        print(seconds_to_formatted_time(120))
        print(seconds_to_formatted_time(121))
        print(seconds_to_formatted_time(179))
        print(seconds_to_formatted_time(180))
        print(seconds_to_formatted_time(181))
        print(seconds_to_formatted_time(239))
        print(seconds_to_formatted_time(240))
        print(seconds_to_formatted_time(241))
        print(seconds_to_formatted_time(3599))
        print(seconds_to_formatted_time(3600))
        print(seconds_to_formatted_time(3601))
        print(seconds_to_formatted_time(7199))
        print(seconds_to_formatted_time(7200))
        print(seconds_to_formatted_time(7201))
        print(seconds_to_formatted_time(86399))
        print(seconds_to_formatted_time(86400))
        print(seconds_to_formatted_time(86401))
        print(seconds_to_formatted_time(172799))
        print(seconds_to_formatted_time(172800))
        print(seconds_to_formatted_time(172801))
        print(seconds_to_formatted_time(259199))
        print(seconds_to_formatted_time(259200))
        print(seconds_to_formatted_time(259201))