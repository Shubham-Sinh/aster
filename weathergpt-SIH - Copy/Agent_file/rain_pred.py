"""def rain_predictes(data):
    hourly=data["hourly"]
    rain=data["rain"]
    rainfall_1h=sum(rain[-1:])
    rainfall_6h=sum(rain[-6:])
    rainfall_24h=sum(rain[-24:])
    rainfall_3day=sum(rain[-72:])
    temperature=hourly["temperature_2m"][-1]
    humidity=hourly["relative_humadity_2m"][-1]
    pressure=hourly["pressure_msl"][-1]
    wind_speed=hourly["wing_speed_10m"][-1]
    cloud_cover=hourly["cloud_cover"][-1]
    return {
        "rainfall_1h":rainfall_1h,
        "rainfall_6h":rainfall_6h,
        "rainfall_24h":rainfall_24h,
        "rainfall_3day":rainfall_3day,
        "temperature":temperature,
        "humidity":humidity,
        "pressure":pressure,
        "wind_speed":wind_speed,
        "cloud_cover":cloud_cover
    }  """
def rain_predictes(data):
    hourly = data.get("hourly", data)

    rain = hourly.get("rain", [0.0])
    if not rain:
        rain = [0.0]

    rainfall_1h = float(sum(rain[-1:]))
    rainfall_6h = float(sum(rain[-6:]))
    rainfall_24h = float(sum(rain[-24:]))
    rainfall_3day = float(sum(rain[-72:]))

    # Helper function taaki list empty hone par IndexError na aaye
    def get_last_val(key, default_val=0.0):
        lst = hourly.get(key, [])
        return float(lst[-1]) if lst else float(default_val)

    temperature = get_last_val("temperature_2m", 25.0)
    humidity = get_last_val("relative_humidity_2m", 70.0)
    pressure = get_last_val("pressure_msl", 1013.0)
    wind_speed = get_last_val("wind_speed_10m", 5.0)
    cloud_cover = get_last_val("cloud_cover", 50.0)

    return {
        "rainfall_1h": rainfall_1h,
        "rainfall_6h": rainfall_6h,
        "rainfall_24h": rainfall_24h,
        "rainfall_3day": rainfall_3day,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed,
        "cloud_cover": cloud_cover
    }