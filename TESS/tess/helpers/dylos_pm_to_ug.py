def small_to_ug(small, large):
    return round((small - large) / 100)

def large_to_ug(large):
    return round(large / 3)

def series_small_large(small, large):
    return pd.Series({"small_ug": small_to_ug(small, large), "large_ug": large_to_ug(large)})

def pm25_to_aqi(pm25):
    aqi = ihigh = ilow = chigh = clow = 0.0

    if 0.0 <= pm25 and pm25 <= 15.4:
        # Good
        ihigh = 50
        ilow = 0
        chigh = 15.4
        clow = 0
    elif 15.5 <= pm25 and pm25 <= 40.4:
        # Moderate
        ihigh = 100
        ilow = 51
        chigh = 40.4
        clow = 15.5
    elif 40.5 <= pm25 and pm25 <= 65.4:
        # Unhealthy
        ihigh = 150
        ilow = 101
        chigh = 65.4
        clow = 40.5
    elif 65.5 <= pm25 and pm25 <= 150.4:
        # Very unhealthy
        ihigh = 200
        ilow = 151
        chigh = 150.4
        clow = 65.5
    elif 150.5 <= pm25 and pm25 <= 250.4:
        # Hazardous
        ihigh = 300
        ilow = 201
        chigh = 250.4
        clow = 150.5
    elif 250.5 <= pm25 and pm25 <= 350.4:
        # Hazardous
        ihigh = 400
        ilow = 301
        chigh = 350.4
        clow = 250.5
    elif 350.5 <= pm25 and pm25 <= 500.4:
        # Hazardous
        ihigh = 500
        ilow = 401
        chigh = 500.4
        clow = 350.5
    else:
        return aqi

    aqi = ((ihigh - ilow) / (chigh - clow)) * (pm25 - clow) + ilow

    return round(aqi)