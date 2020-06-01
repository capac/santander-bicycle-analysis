# /usr/bin/env python3

from itertools import islice
import numpy as np


# group elements of list in tuples of four elements each for
# sum, difference, latitude and longitude (in Mercator coords)
def station_chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


# return a list of dictorionaries, each one of which has as key the time
# and as value a dictionary with sum_flux, diff_flux, lat and long values
def bike_flux(flux_df):
    bike_flux_list = []
    for row in flux_df.itertuples():
        sum_flux, diff_flux, lat, long = list(
            map(tuple, zip(*station_chunk(row[1:], 4))))
        sum_flux = list(np.array(sum_flux)/1e2)
        diff_flux = list(np.array(diff_flux)/1e2)
        bike_flux_list.append(
            {row[0]: {'sum_flux': sum_flux, 'diff': diff_flux,
                      'lat': lat, 'long': long}})
    return bike_flux_list


def select_time():
    selected = bike_flux_list
    hour_interval = hour_interval_selector.value
    min_flux = flux_slider.value

    selected_df = pd.DataFrame(selected[hour_interval].values())
    selected_df = selected_df[(selected_df['sum_flux'] >= min_flux)]

    print('Hour interval =', hour_interval)
    print('Min flux =', min_flux)

    return selected_df


def update():
    df = select_time()

    source.data = dict(
        lat=df['lat'],
        long=df['long'],
        sum_flux=df['sum_flux'],
        diff_flux=df['diff']
    )
