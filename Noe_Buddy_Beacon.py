# Noe_Buddy_Beacon.py
# Version: Public Release Tutorial Build 1.1
#
# ============================================================
# NOE BUDDY BEACON
# iPhone + Pythonista 3 + iOS Shortcuts safety check-in beacon
# ============================================================
#
# WHAT THIS DOES
# --------------
# This script is designed for a consent-based buddy system.
#
# A trusted contact sends your iPhone a secret phrase such as:
#
#     NOE CHECK IN 7391
#
# iOS Shortcuts detects that text message, runs this Pythonista script,
# then sends the script's output back to your trusted contact.
#
# The script does the heavy lifting:
#   - gets your current latitude and longitude
#   - estimates a cautious search radius in metres
#   - reverse-geocodes the nearest readable place/address
#   - adds Apple Maps, Google Maps, OpenStreetMap, and geo: links
#   - adds battery/device/iOS/location-permission context
#   - adds motion/stillness clues if available
#   - adds a UK National Grid reference when inside Great Britain
#   - saves local logs in Pythonista Documents
#   - copies the finished message to clipboard
#   - prints the finished message so Shortcuts can send it
#
# The script does NOT send texts by itself.
# Shortcuts is the courier. Pythonista is the beacon engine.
#
#
# IMPORTANT CONSENT + SAFETY NOTES
# --------------------------------
# Use this only on your own phone.
# Use it only with trusted people who have agreed to be safety contacts.
# Do not use it to track, control, stalk, test, or locate another person.
#
# This is not a replacement for emergency services, Apple Emergency SOS,
# Find My, live location sharing, or Check In. It is an extra safety lantern.
#
# The nearest address/place is reverse-geocoded from coordinates. It may not
# be the exact room, floor, ward, entrance, building, or side of the road.
# The search radius is the useful truth. Do not treat the decimal coordinates
# as exact beyond the stated radius.
#
# If you are in immediate danger, use your local emergency service number
# if you can. In the UK that is 999 or 112.
#
#
# WHAT YOU NEED
# -------------
# 1. iPhone
# 2. Pythonista 3 installed
# 3. iOS Shortcuts app
# 4. Location Services enabled for Pythonista
# 5. A trusted contact who has agreed to receive beacon messages
#
#
# STEP 1: INSTALL THIS SCRIPT IN PYTHONISTA
# ----------------------------------------
# 1. Open Pythonista 3.
# 2. Create a new Python file.
# 3. Name it:
#
#        Noe_Buddy_Beacon.py
#
# 4. Paste this whole script into that file.
# 5. Run it once manually.
# 6. When iOS asks for location permission, allow it.
# 7. Recommended:
#
#        Settings > Privacy & Security > Location Services > Pythonista
#
#    Set:
#
#        Location Access: While Using the App or Always if available
#        Precise Location: ON
#
# The first manual run is important. It wakes up permissions while you are safe.
#
#
# STEP 2: CREATE THE SHORTCUT AUTOMATION
# -------------------------------------
# 1. Open the Shortcuts app.
# 2. Tap Automation.
# 3. Tap + or New Automation.
# 4. Choose Message.
# 5. Set Sender to your trusted contact.
# 6. Set Message Contains to a secret phrase, for example:
#
#        NOE CHECK IN 7391
#
#    Do not use a normal phrase like "check in" by itself.
#    Use something unlikely to be typed accidentally.
#
# 7. Choose Run Immediately if iOS offers it.
# 8. Turn off "Ask Before Running" if that option appears.
#
#
# STEP 3: ADD THE ACTIONS
# -----------------------
# Add this action:
#
#   Run Pythonista Script
#
# Choose:
#
#   Noe_Buddy_Beacon.py
#
# If options appear, use:
#
#   Run in Pythonista: OFF, if available
#   Show When Run: OFF, if available
#
# Then add:
#
#   Send Message
#
# Message body:
#
#   Pythonista Script Result
#
# Recipient:
#
#   Your trusted contact
#
#
# BACKUP SHORTCUT METHOD
# ----------------------
# If "Pythonista Script Result" does not appear or behaves oddly:
#
# Actions:
#
#   1. Run Pythonista Script: Noe_Buddy_Beacon.py
#   2. Wait: 1 second
#   3. Get Clipboard
#   4. Send Message
#
# Message body:
#
#   Clipboard
#
# Recipient:
#
#   Your trusted contact
#
# The script both prints the beacon message and copies it to clipboard, so
# either route should work.
#
#
# STEP 4: TEST IT SAFELY
# ----------------------
# Test while calm, charged, and not in an emergency.
#
# Ask your trusted contact to text exactly:
#
#   NOE CHECK IN 7391
#
# Confirm they receive a reply containing:
#
#   - nearest readable place/address
#   - latitude and longitude
#   - search radius in metres
#   - timestamp
#   - maps links
#   - battery/device/location quality details
#
# Then test again:
#
#   - indoors
#   - outdoors
#   - with Wi-Fi on
#   - with mobile data on
#   - after locking your phone
#
# iOS behaviour can change depending on permissions, lock state, signal,
# battery, Focus modes, and whether Shortcuts decides an action needs approval.
#
#
# RECOMMENDED SECRET PHRASE IDEAS
# -------------------------------
# Use a phrase that is easy for your buddy to remember but hard to trigger
# accidentally.
#
# Examples:
#
#   NOE CHECK IN 7391
#   DYLAN BEACON WAKE 7391
#   BUDDY BEACON PLEASE 7391
#   SAFETY LANTERN 7391
#
# Avoid:
#
#   check in
#   where are you
#   are you okay
#
#
# WHAT THE REPLY MEANS
# --------------------
# Example:
#
#   Lat: 54.29752032
#   Lon: -0.42562925
#   Search within about ±7.6 m
#
# The coordinate is the centre of the phone's best estimate.
# The radius is the uncertainty bubble.
#
# A person trying to find you should search within that radius and use
# the readable place/address, maps link, landmarks, calls, sounds, staff,
# reception, security, and live updates if available.
#
#
# LIMITATIONS
# -----------
# This cannot work if:
#
#   - the phone is powered off
#   - the battery is dead
#   - there is no signal/data route for the reply
#   - iOS blocks or delays the automation
#   - location permission is denied
#   - the phone is shielded from useful location signals
#
# Indoors, GPS may not know exact room or floor.
# Altitude can be noisy.
# Address lookup can be approximate.
# SMS may split long messages.
#
#
# PUBLIC RELEASE PRIVACY DEFAULTS
# -------------------------------
# By default, this script hides the private device name.
# It sends device model/iOS/battery/location quality because that can help a
# trusted contact understand whether the beacon is fresh and usable.
#
# You can edit the SETTINGS section below if you want shorter output.
#
#
# QUICK SETUP SUMMARY
# -------------------
# Pythonista:
#
#   Save this file as Noe_Buddy_Beacon.py and run once.
#
# Shortcuts:
#
#   Automation > Message
#   Sender = trusted contact
#   Message Contains = NOE CHECK IN 7391
#   Run Immediately
#
# Actions:
#
#   Run Pythonista Script: Noe_Buddy_Beacon.py
#   Send Message: Pythonista Script Result to trusted contact
#
# Backup:
#
#   Run Pythonista Script
#   Wait 1 second
#   Get Clipboard
#   Send Clipboard to trusted contact
#
# ============================================================
# END OF PUBLIC SETUP GUIDE
# ============================================================
#
import datetime
import json
import math
import os
import platform
import sys
import time
import traceback

try:
    import location
except Exception:
    location = None

try:
    import clipboard
except Exception:
    clipboard = None

try:
    import motion
except Exception:
    motion = None

try:
    import objc_util
except Exception:
    objc_util = None


# -----------------------------
# SETTINGS YOU MAY EDIT
# -----------------------------

BEACON_NAME = "AUTO BUDDY BEACON"

# Keep this true so the Shortcut can use either:
#   - Pythonista Script Result from print()
#   - Get Clipboard as a backup
COPY_TO_CLIPBOARD = True

# How many GPS/location samples to gather.
# More samples = better reliability, but slower.
SAMPLES = 8

# Seconds between location samples.
SAMPLE_DELAY_SECONDS = 1.0

# If a fix reaches this accuracy after a few samples, stop early.
TARGET_ACCURACY_METRES = 8.0

# Reject very poor samples over this accuracy unless they are all we have.
MAX_ACCEPTABLE_ACCURACY_METRES = 250.0

# Use reverse geocoding to turn coordinates into a readable place/address.
USE_REVERSE_GEOCODE = True

# Include a short motion stillness estimate, if Pythonista can access motion sensors.
USE_MOTION_SNAPSHOT = True

# Save latest message and JSON packet locally in Pythonista Documents.
SAVE_LOCAL_FILES = True

# Local save folder under Pythonista Documents.
SAVE_FOLDER_NAME = "Noe_Buddy_Beacon"

# Keep SMS-ish message compact. If False, prints a longer JSON packet instead.
# For auto-reply texts, leave True.
OUTPUT_HUMAN_MESSAGE = True

# If a phone number or name is not hard-coded here, Shortcuts should choose the recipient.
# Usually best: leave as None and let the Shortcut send to your trusted contact.
TRUSTED_CONTACT_LABEL = None


# -----------------------------
# BASIC HELPERS
# -----------------------------

EARTH_RADIUS_M = 6371008.8

WGS84_A = 6378137.0
WGS84_F = 1 / 298.257223563
WGS84_E2 = WGS84_F * (2 - WGS84_F)


def now_local_dt():
    return datetime.datetime.now().astimezone()


def now_utc_dt():
    return datetime.datetime.now(datetime.timezone.utc)


def iso_local():
    return now_local_dt().isoformat()


def iso_utc():
    return now_utc_dt().isoformat()


def safe_float(value, default=None):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def safe_round(value, digits=1, default="unknown"):
    try:
        if value is None:
            return default
        return round(float(value), digits)
    except Exception:
        return default


def metres_to_miles(m):
    return float(m) / 1609.344


def mps_to_mph(mps):
    return float(mps) * 2.2369362921


def mps_to_kph(mps):
    return float(mps) * 3.6


def haversine_m(lat1, lon1, lat2, lon2):
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2.0) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dl / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_M * c


def latlon_to_local_xy(lat, lon, origin_lat, origin_lon):
    # Good local approximation for small distances.
    x = math.radians(lon - origin_lon) * EARTH_RADIUS_M * math.cos(math.radians(origin_lat))
    y = math.radians(lat - origin_lat) * EARTH_RADIUS_M
    return x, y


def local_xy_to_latlon(x, y, origin_lat, origin_lon):
    lat = origin_lat + math.degrees(y / EARTH_RADIUS_M)
    lon = origin_lon + math.degrees(x / (EARTH_RADIUS_M * math.cos(math.radians(origin_lat))))
    return lat, lon


def lla_to_ecef(lat_deg, lon_deg, alt_m):
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)

    n = WGS84_A / math.sqrt(1.0 - WGS84_E2 * sin_lat * sin_lat)

    x = (n + alt_m) * cos_lat * math.cos(lon)
    y = (n + alt_m) * cos_lat * math.sin(lon)
    z = (n * (1.0 - WGS84_E2) + alt_m) * sin_lat
    return x, y, z


def quality_label(acc_m):
    if acc_m is None:
        return "unknown"
    acc_m = float(acc_m)
    if acc_m <= 5:
        return "excellent"
    if acc_m <= 15:
        return "good"
    if acc_m <= 50:
        return "rough but useful"
    if acc_m <= 250:
        return "wide search area"
    return "very rough"


def dms(value, is_lat=True):
    direction = ""
    if is_lat:
        direction = "N" if value >= 0 else "S"
    else:
        direction = "E" if value >= 0 else "W"

    v = abs(float(value))
    deg = int(v)
    minutes_float = (v - deg) * 60.0
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60.0

    return '{}°{}\'{:.3f}" {}'.format(deg, minutes, seconds, direction)


def geohash_encode(latitude, longitude, precision=11):
    # Tiny built-in geohash encoder.
    base32 = "0123456789bcdefghjkmnpqrstuvwxyz"
    lat_interval = [-90.0, 90.0]
    lon_interval = [-180.0, 180.0]

    geohash = []
    bit = 0
    ch = 0
    even = True

    bits = [16, 8, 4, 2, 1]

    while len(geohash) < precision:
        if even:
            mid = sum(lon_interval) / 2.0
            if longitude >= mid:
                ch |= bits[bit]
                lon_interval[0] = mid
            else:
                lon_interval[1] = mid
        else:
            mid = sum(lat_interval) / 2.0
            if latitude >= mid:
                ch |= bits[bit]
                lat_interval[0] = mid
            else:
                lat_interval[1] = mid

        even = not even

        if bit < 4:
            bit += 1
        else:
            geohash.append(base32[ch])
            bit = 0
            ch = 0

    return "".join(geohash)


# -----------------------------
# UK NATIONAL GRID
# -----------------------------

def wgs84_to_osgb36_latlon(lat, lon, h=0.0):
    """
    Approx conversion WGS84 -> OSGB36 using Helmert transform.
    Useful for UK grid references, not a replacement for GPS uncertainty radius.
    """
    # WGS84 ellipsoid
    a = 6378137.0
    b = 6356752.3141
    e2 = 1.0 - (b*b)/(a*a)

    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    nu = a / math.sqrt(1.0 - e2 * math.sin(lat_rad)**2)

    x1 = (nu + h) * math.cos(lat_rad) * math.cos(lon_rad)
    y1 = (nu + h) * math.cos(lat_rad) * math.sin(lon_rad)
    z1 = ((1.0 - e2) * nu + h) * math.sin(lat_rad)

    # Helmert transform WGS84 -> OSGB36
    tx = -446.448
    ty = 125.157
    tz = -542.060
    s = 20.4894 * 1e-6
    rx = math.radians(-0.1502 / 3600.0)
    ry = math.radians(-0.2470 / 3600.0)
    rz = math.radians(-0.8421 / 3600.0)

    x2 = tx + (1+s)*x1 + (-rz)*y1 + (ry)*z1
    y2 = ty + (rz)*x1 + (1+s)*y1 + (-rx)*z1
    z2 = tz + (-ry)*x1 + (rx)*y1 + (1+s)*z1

    # Airy 1830 ellipsoid
    a2 = 6377563.396
    b2 = 6356256.909
    e22 = 1.0 - (b2*b2)/(a2*a2)

    p = math.sqrt(x2*x2 + y2*y2)
    lat2 = math.atan2(z2, p * (1.0 - e22))

    for _ in range(10):
        nu2 = a2 / math.sqrt(1.0 - e22 * math.sin(lat2)**2)
        lat2 = math.atan2(z2 + e22 * nu2 * math.sin(lat2), p)

    lon2 = math.atan2(y2, x2)
    return math.degrees(lat2), math.degrees(lon2)


def osgb36_to_easting_northing(lat, lon):
    """
    OSGB36 lat/lon -> British National Grid easting/northing.
    """
    lat = math.radians(lat)
    lon = math.radians(lon)

    a = 6377563.396
    b = 6356256.909
    f0 = 0.9996012717
    lat0 = math.radians(49.0)
    lon0 = math.radians(-2.0)
    n0 = -100000.0
    e0 = 400000.0
    e2 = 1.0 - (b*b)/(a*a)
    n = (a - b) / (a + b)

    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    tan_lat = math.tan(lat)

    nu = a * f0 / math.sqrt(1.0 - e2 * sin_lat*sin_lat)
    rho = a * f0 * (1.0 - e2) / ((1.0 - e2 * sin_lat*sin_lat) ** 1.5)
    eta2 = nu / rho - 1.0

    ma = (1+n+(5.0/4.0)*n*n+(5.0/4.0)*n**3) * (lat-lat0)
    mb = (3*n+3*n*n+(21.0/8.0)*n**3) * math.sin(lat-lat0) * math.cos(lat+lat0)
    mc = ((15.0/8.0)*n*n+(15.0/8.0)*n**3) * math.sin(2*(lat-lat0)) * math.cos(2*(lat+lat0))
    md = (35.0/24.0)*n**3 * math.sin(3*(lat-lat0)) * math.cos(3*(lat+lat0))
    m = b * f0 * (ma - mb + mc - md)

    dl = lon - lon0

    i = m + n0
    ii = nu/2.0 * sin_lat * cos_lat
    iii = nu/24.0 * sin_lat * cos_lat**3 * (5.0 - tan_lat**2 + 9.0*eta2)
    iiia = nu/720.0 * sin_lat * cos_lat**5 * (61.0 - 58.0*tan_lat**2 + tan_lat**4)
    iv = nu * cos_lat
    v = nu/6.0 * cos_lat**3 * (nu/rho - tan_lat**2)
    vi = nu/120.0 * cos_lat**5 * (5.0 - 18.0*tan_lat**2 + tan_lat**4 + 14.0*eta2 - 58.0*tan_lat**2*eta2)

    northing = i + ii*dl**2 + iii*dl**4 + iiia*dl**6
    easting = e0 + iv*dl + v*dl**3 + vi*dl**5

    return easting, northing


def grid_ref_from_e_n(easting, northing, digits=10):
    """
    Convert British National Grid easting/northing to grid reference.
    digits=10 -> 1m grid ref, but real uncertainty is still GPS radius.
    """
    if easting < 0 or northing < 0 or easting >= 700000 or northing >= 1300000:
        return None

    e100k = int(easting) // 100000
    n100k = int(northing) // 100000

    # Letter grid, skipping I.
    l1 = (19 - n100k) - (19 - n100k) % 5 + ((e100k + 10) // 5)
    l2 = ((19 - n100k) * 5) % 25 + e100k % 5

    def letter(index):
        return chr(index + ord("A") + (1 if index >= 8 else 0))

    letters = letter(l1) + letter(l2)

    rem_e = int(round(easting)) % 100000
    rem_n = int(round(northing)) % 100000

    half = digits // 2
    scale = 10 ** (5 - half)

    e_part = int(rem_e // scale)
    n_part = int(rem_n // scale)

    return "{} {:0{w}d} {:0{w}d}".format(letters, e_part, n_part, w=half)


def maybe_uk_grid(lat, lon, alt):
    # Rough GB bounding box. Not NI.
    if not (49.0 <= lat <= 61.0 and -8.5 <= lon <= 2.5):
        return None

    try:
        osgb_lat, osgb_lon = wgs84_to_osgb36_latlon(lat, lon, alt)
        e, n = osgb36_to_easting_northing(osgb_lat, osgb_lon)
        grid = grid_ref_from_e_n(e, n, 10)
        if grid is None:
            return None
        return {
            "grid_ref_10_digit": grid,
            "easting_m": round(e, 3),
            "northing_m": round(n, 3),
            "note": "Derived from GPS coordinates. Use the rescue radius as true uncertainty."
        }
    except Exception:
        return None


# -----------------------------
# LOCATION
# -----------------------------

def valid_location(loc):
    if not loc:
        return False

    lat = safe_float(loc.get("latitude"))
    lon = safe_float(loc.get("longitude"))
    acc = safe_float(loc.get("horizontal_accuracy"))

    if lat is None or lon is None or acc is None:
        return False

    if acc < 0:
        return False

    if not (-90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0):
        return False

    return True


def collect_locations():
    if location is None:
        raise RuntimeError("Pythonista location module unavailable.")

    samples = []
    raw_polls = 0

    location.start_updates()

    try:
        for i in range(SAMPLES):
            time.sleep(SAMPLE_DELAY_SECONDS)
            raw_polls += 1
            loc = location.get_location()

            if valid_location(loc):
                loc = dict(loc)
                loc["_captured_local"] = iso_local()
                loc["_captured_unix_time"] = time.time()

                acc = safe_float(loc.get("horizontal_accuracy"), 999999.0)
                if acc <= MAX_ACCEPTABLE_ACCURACY_METRES:
                    samples.append(loc)
                elif not samples:
                    # Keep one poor sample if it is all we have.
                    samples.append(loc)

                if len(samples) >= 3 and acc <= TARGET_ACCURACY_METRES:
                    break
    finally:
        try:
            location.stop_updates()
        except Exception:
            pass

    if not samples:
        raise RuntimeError("No valid location fix.")

    return samples, raw_polls


def robust_fix(samples):
    samples = [s for s in samples if valid_location(s)]
    if not samples:
        raise RuntimeError("No valid samples after filtering.")

    samples.sort(key=lambda s: safe_float(s.get("horizontal_accuracy"), 999999.0))

    best = samples[0]
    origin_lat = safe_float(best["latitude"])
    origin_lon = safe_float(best["longitude"])

    kept = []
    rejected = []

    for s in samples:
        lat = safe_float(s["latitude"])
        lon = safe_float(s["longitude"])
        acc = max(safe_float(s.get("horizontal_accuracy"), 999999.0), 1.0)

        distance = haversine_m(origin_lat, origin_lon, lat, lon)

        # Keep samples that agree with the best sample.
        if distance <= max(30.0, acc * 3.0):
            kept.append(s)
        else:
            rejected.append(s)

    if not kept:
        kept = [best]

    weight_sum = 0.0
    weighted_x = 0.0
    weighted_y = 0.0
    weighted_alt = 0.0

    for s in kept:
        lat = safe_float(s["latitude"])
        lon = safe_float(s["longitude"])
        alt = safe_float(s.get("altitude"), 0.0)
        acc = max(safe_float(s.get("horizontal_accuracy"), 999999.0), 1.0)
        w = 1.0 / (acc * acc)

        x, y = latlon_to_local_xy(lat, lon, origin_lat, origin_lon)
        weighted_x += x * w
        weighted_y += y * w
        weighted_alt += alt * w
        weight_sum += w

    mean_x = weighted_x / weight_sum
    mean_y = weighted_y / weight_sum
    mean_alt = weighted_alt / weight_sum

    fix_lat, fix_lon = local_xy_to_latlon(mean_x, mean_y, origin_lat, origin_lon)

    distances = []
    accuracies = []
    vertical_accuracies = []

    for s in kept:
        lat = safe_float(s["latitude"])
        lon = safe_float(s["longitude"])
        acc = safe_float(s.get("horizontal_accuracy"), 999999.0)
        distances.append(haversine_m(fix_lat, fix_lon, lat, lon))
        accuracies.append(acc)

        v_acc = safe_float(s.get("vertical_accuracy"))
        if v_acc is not None and v_acc >= 0:
            vertical_accuracies.append(v_acc)

    accuracies_sorted = sorted(accuracies)
    distances_sorted = sorted(distances)

    best_acc = accuracies_sorted[0]
    median_acc = accuracies_sorted[len(accuracies_sorted) // 2]
    spread_max = max(distances) if distances else 0.0
    spread_mean = sum(distances) / len(distances) if distances else 0.0
    spread_rms = math.sqrt(sum(d*d for d in distances) / len(distances)) if distances else 0.0

    # Conservative rescue radius. The centre point + this radius is the true useful output.
    rescue_radius = max(best_acc, median_acc, spread_max + best_acc, best_acc + 3.0)

    speed = safe_float(best.get("speed"))
    course = safe_float(best.get("course"))
    if course is not None and course < 0:
        course = None

    return {
        "latitude": fix_lat,
        "longitude": fix_lon,
        "altitude": mean_alt,
        "rescue_radius_m": rescue_radius,
        "best_reported_accuracy_m": best_acc,
        "median_reported_accuracy_m": median_acc,
        "sample_spread_max_m": spread_max,
        "sample_spread_mean_m": spread_mean,
        "sample_spread_rms_m": spread_rms,
        "samples_used": len(kept),
        "samples_total": len(samples),
        "samples_rejected": len(rejected),
        "vertical_accuracy_best_m": min(vertical_accuracies) if vertical_accuracies else None,
        "best_raw_sample": best,
        "speed_mps": speed if speed is not None and speed >= 0 else None,
        "course_degrees_true_north": course,
    }


def reverse_geocode_text(lat, lon):
    if not USE_REVERSE_GEOCODE or location is None:
        return "unavailable"

    try:
        result = location.reverse_geocode({
            "latitude": lat,
            "longitude": lon,
        })

        if isinstance(result, list) and result:
            result = result[0]

        if isinstance(result, dict):
            lines = result.get("FormattedAddressLines")
            if lines:
                return ", ".join(str(x) for x in lines)

            parts = []
            for key in ["Name", "Street", "City", "State", "ZIP", "Country", "CountryCode"]:
                if result.get(key):
                    parts.append(str(result[key]))
            if parts:
                return ", ".join(parts)

            return json.dumps(result, sort_keys=True)

        return str(result)

    except Exception as e:
        return "reverse geocode failed: {}".format(e)


# -----------------------------
# DEVICE CONTEXT
# -----------------------------

def get_device_context():
    ctx = {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_version": sys.version,
        "objc_available": objc_util is not None,
    }

    if objc_util is None:
        return ctx

    try:
        UIDevice = objc_util.ObjCClass("UIDevice")
        device = UIDevice.currentDevice()
        device.setBatteryMonitoringEnabled_(True)

        state_map = {
            0: "unknown",
            1: "unplugged",
            2: "charging",
            3: "full",
        }

        battery_level = float(device.batteryLevel())
        if battery_level >= 0:
            ctx["battery_percent"] = round(battery_level * 100.0, 1)
        else:
            ctx["battery_percent"] = "unknown"

        ctx["battery_state"] = state_map.get(int(device.batteryState()), "unknown")
        ctx["device_model"] = str(device.model())
        ctx["device_localized_model"] = str(device.localizedModel())
        ctx["ios_system_name"] = str(device.systemName())
        ctx["ios_system_version"] = str(device.systemVersion())
    except Exception:
        ctx["battery_percent"] = "unknown"
        ctx["battery_state"] = "unknown"

    try:
        NSProcessInfo = objc_util.ObjCClass("NSProcessInfo")
        info = NSProcessInfo.processInfo()

        thermal_map = {
            0: "nominal",
            1: "fair",
            2: "serious",
            3: "critical",
        }

        ctx["low_power_mode_enabled"] = bool(info.isLowPowerModeEnabled())
        ctx["thermal_state"] = thermal_map.get(int(info.thermalState()), "unknown")
        ctx["processor_count"] = int(info.processorCount())
        ctx["active_processor_count"] = int(info.activeProcessorCount())
        ctx["physical_memory_bytes"] = int(info.physicalMemory())
        ctx["system_uptime_seconds"] = float(info.systemUptime())
    except Exception:
        pass

    try:
        NSBundle = objc_util.ObjCClass("NSBundle")
        bundle = NSBundle.mainBundle()
        info_dict = bundle.infoDictionary()
        ctx["app_bundle_identifier"] = str(bundle.bundleIdentifier())
        ctx["app_bundle_name"] = str(info_dict.objectForKey_("CFBundleName"))
        ctx["app_bundle_short_version"] = str(info_dict.objectForKey_("CFBundleShortVersionString"))
        ctx["app_bundle_version"] = str(info_dict.objectForKey_("CFBundleVersion"))
    except Exception:
        pass

    return ctx


def get_location_permission_context():
    ctx = {
        "available": False
    }

    if objc_util is None:
        return ctx

    try:
        CLLocationManager = objc_util.ObjCClass("CLLocationManager")
        manager = CLLocationManager.alloc().init()

        auth_map = {
            0: "not_determined",
            1: "restricted",
            2: "denied",
            3: "authorized_always",
            4: "authorized_when_in_use",
        }

        accuracy_map = {
            0: "full_accuracy",
            1: "reduced_accuracy",
        }

        try:
            status_raw = int(CLLocationManager.authorizationStatus())
        except Exception:
            status_raw = None

        try:
            services_enabled = bool(CLLocationManager.locationServicesEnabled())
        except Exception:
            services_enabled = None

        try:
            accuracy_raw = int(manager.accuracyAuthorization())
        except Exception:
            accuracy_raw = None

        ctx = {
            "available": True,
            "location_services_enabled": services_enabled,
            "authorization_status_raw": status_raw,
            "authorization_status": auth_map.get(status_raw, "unknown"),
            "accuracy_authorization_raw": accuracy_raw,
            "accuracy_authorization": accuracy_map.get(accuracy_raw, "unknown"),
        }

    except Exception as e:
        ctx["error"] = str(e)

    return ctx


def get_motion_snapshot():
    if not USE_MOTION_SNAPSHOT or motion is None:
        return {
            "available": False,
            "note": "motion module unavailable or disabled"
        }

    try:
        motion.start_updates()
        max_user_accel = 0.0
        last_gravity = None
        last_user = None
        last_attitude = None

        start = time.time()
        while time.time() - start < 2.0:
            time.sleep(0.2)
            try:
                g = motion.get_gravity()
                u = motion.get_user_acceleration()
                a = motion.get_attitude()
            except Exception:
                continue

            if g:
                last_gravity = tuple(float(x) for x in g)
            if u:
                last_user = tuple(float(x) for x in u)
                mag = math.sqrt(sum(float(x)*float(x) for x in u))
                max_user_accel = max(max_user_accel, mag)
            if a:
                last_attitude = tuple(float(x) for x in a)

        if max_user_accel < 0.03:
            stillness = "very_still"
        elif max_user_accel < 0.12:
            stillness = "slight_motion"
        else:
            stillness = "moving_or_jostled"

        return {
            "available": True,
            "sample_seconds": 2.0,
            "stillness_estimate": stillness,
            "max_user_acceleration_g": max_user_accel,
            "gravity_xyz_g": last_gravity,
            "user_acceleration_xyz_g": last_user,
            "attitude_roll_pitch_yaw_radians": last_attitude,
            "note": "Motion values are phone orientation/movement clues, not medical data."
        }

    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }
    finally:
        try:
            motion.stop_updates()
        except Exception:
            pass


# -----------------------------
# PACKET + MESSAGE BUILDING
# -----------------------------

def build_maps(lat, lon, radius_m):
    return {
        "apple_maps": "http://maps.apple.com/?ll={:.8f},{:.8f}&z=19".format(lat, lon),
        "google_maps": "https://www.google.com/maps/search/?api=1&query={:.8f},{:.8f}".format(lat, lon),
        "openstreetmap": "https://www.openstreetmap.org/?mlat={:.8f}&mlon={:.8f}#map=19/{:.8f}/{:.8f}".format(
            lat, lon, lat, lon
        ),
        "geo_uri": "geo:{:.8f},{:.8f};u={:.1f}".format(lat, lon, radius_m),
    }


def build_packet():
    samples, raw_polls = collect_locations()
    fix = robust_fix(samples)

    lat = fix["latitude"]
    lon = fix["longitude"]
    alt = fix["altitude"]
    radius_m = fix["rescue_radius_m"]

    ecef = lla_to_ecef(lat, lon, alt)
    maps = build_maps(lat, lon, radius_m)
    place = reverse_geocode_text(lat, lon)
    grid = maybe_uk_grid(lat, lon, alt)

    speed_mps = fix.get("speed_mps")
    movement = {
        "speed_mps": speed_mps,
        "speed_mph": mps_to_mph(speed_mps) if speed_mps is not None else None,
        "speed_kph": mps_to_kph(speed_mps) if speed_mps is not None else None,
        "course_degrees_true_north": fix.get("course_degrees_true_north"),
        "motion_snapshot": get_motion_snapshot(),
    }

    created_local = iso_local()
    created_utc = iso_utc()
    created_unix = time.time()

    packet = {
        "packet_type": "Noe_Buddy_Beacon",
        "packet_version": "1.0",
        "created_local": created_local,
        "created_utc": created_utc,
        "created_unix_time": created_unix,

        "find_me": {
            "latitude_degrees": lat,
            "longitude_degrees": lon,
            "latitude_dms": dms(lat, True),
            "longitude_dms": dms(lon, False),
            "altitude_metres": alt,
            "rescue_search_radius_metres": radius_m,
            "rescue_search_radius_miles": metres_to_miles(radius_m),
            "quality_label": quality_label(radius_m),
            "geohash_11": geohash_encode(lat, lon, 11),
            "readable_place": place,
            "maps": maps,
            "uk_national_grid": grid,
        },

        "location_quality": {
            "accuracy_note": "Use centre point plus rescue_search_radius_metres. Do not assume the coordinate is exact beyond that radius.",
            "best_reported_horizontal_accuracy_metres": fix["best_reported_accuracy_m"],
            "median_reported_horizontal_accuracy_metres": fix["median_reported_accuracy_m"],
            "sample_spread_max_metres": fix["sample_spread_max_m"],
            "sample_spread_mean_metres": fix["sample_spread_mean_m"],
            "sample_spread_rms_metres": fix["sample_spread_rms_m"],
            "samples_used": fix["samples_used"],
            "samples_total": fix["samples_total"],
            "samples_rejected": fix["samples_rejected"],
            "raw_polls": raw_polls,
            "vertical_accuracy_best_metres": fix["vertical_accuracy_best_m"],
            "best_raw_sample": fix["best_raw_sample"],
        },

        "movement": movement,

        "phone_context": {
            "device": get_device_context(),
            "core_location_permission": get_location_permission_context(),
        },

        "earth_space_math": {
            "ecef_xyz_metres": {
                "x": ecef[0],
                "y": ecef[1],
                "z": ecef[2],
            },
            "precision_note": "Decimal-place precision is not sensor accuracy. Use the rescue radius.",
        },

        "limits": {
            "address_limit": "Readable place/address is reverse-geocoded from coordinates and may not be exact.",
            "indoor_limit": "Phone GPS usually cannot guarantee exact room or floor indoors.",
            "altitude_limit": "Altitude can be noisy; trust vertical accuracy when available.",
            "not_automatic_sending": "This script prepares output only. Shortcuts must send it.",
        },
    }

    return packet


def make_human_message(packet):
    f = packet["find_me"]
    q = packet["location_quality"]
    m = packet.get("movement", {})
    pc = packet.get("phone_context", {})
    device = pc.get("device", {})
    perm = pc.get("core_location_permission", {})

    lat = f["latitude_degrees"]
    lon = f["longitude_degrees"]
    radius = f["rescue_search_radius_metres"]
    quality = f.get("quality_label", "unknown")
    place = f.get("readable_place") or "No readable place returned."
    maps = f.get("maps", {})

    grid = f.get("uk_national_grid")
    grid_line = ""
    if grid and grid.get("grid_ref_10_digit"):
        grid_line = "\nUK grid: {}".format(grid["grid_ref_10_digit"])

    battery = device.get("battery_percent", "unknown")
    battery_state = device.get("battery_state", "unknown")
    ios_name = device.get("ios_system_name", "iOS")
    ios_version = device.get("ios_system_version", "unknown")
    device_model = device.get("device_model", "iPhone")
    thermal = device.get("thermal_state", "unknown")
    low_power = device.get("low_power_mode_enabled", "unknown")

    auth = perm.get("authorization_status", "unknown")
    acc_auth = perm.get("accuracy_authorization", "unknown")

    motion_snapshot = m.get("motion_snapshot", {})
    stillness = motion_snapshot.get("stillness_estimate", "unknown")

    speed_mph = m.get("speed_mph")
    if speed_mph is None:
        speed_text = "unknown"
    else:
        speed_text = "{:.2f} mph".format(speed_mph)

    best_acc = q.get("best_reported_horizontal_accuracy_metres")
    median_acc = q.get("median_reported_horizontal_accuracy_metres")
    samples_used = q.get("samples_used", "unknown")
    samples_total = q.get("samples_total", "unknown")

    return (
        "{name}\n\n"
        "Trusted check-in phrase received. This is an automatic location reply from Dylan's phone.\n\n"
        "Nearest readable place/address:\n"
        "{place}\n\n"
        "Find me / my phone near:\n"
        "Lat: {lat:.8f}\n"
        "Lon: {lon:.8f}\n"
        "Search within about ±{radius:.1f} m ({quality})\n"
        "DMS: {lat_dms}, {lon_dms}"
        "{grid_line}\n\n"
        "Time:\n"
        "Local: {local_time}\n"
        "UTC: {utc_time}\n\n"
        "Maps:\n"
        "Apple: {apple}\n"
        "Google: {google}\n"
        "OSM: {osm}\n\n"
        "Location quality:\n"
        "Best raw accuracy: ±{best_acc:.1f} m\n"
        "Median raw accuracy: ±{median_acc:.1f} m\n"
        "Samples: {samples_used}/{samples_total}\n\n"
        "Phone/context:\n"
        "Battery: {battery}% ({battery_state})\n"
        "Motion: {stillness}\n"
        "Speed: {speed}\n"
        "Location permission: {acc_auth}, {auth}\n"
        "Device: {device_model}, {ios_name} {ios_version}\n"
        "Low Power Mode: {low_power}\n"
        "Thermal: {thermal}\n\n"
        "Important: address is derived from coordinates. Use the search radius, not the address alone. "
        "GPS may not identify exact room/floor indoors."
    ).format(
        name=BEACON_NAME,
        place=place,
        lat=lat,
        lon=lon,
        radius=radius,
        quality=quality,
        lat_dms=f.get("latitude_dms", "unknown"),
        lon_dms=f.get("longitude_dms", "unknown"),
        grid_line=grid_line,
        local_time=packet.get("created_local"),
        utc_time=packet.get("created_utc"),
        apple=maps.get("apple_maps", "unavailable"),
        google=maps.get("google_maps", "unavailable"),
        osm=maps.get("openstreetmap", "unavailable"),
        best_acc=float(best_acc) if best_acc is not None else 999999.0,
        median_acc=float(median_acc) if median_acc is not None else 999999.0,
        samples_used=samples_used,
        samples_total=samples_total,
        battery=battery,
        battery_state=battery_state,
        stillness=stillness,
        speed=speed_text,
        acc_auth=acc_auth,
        auth=auth,
        device_model=device_model,
        ios_name=ios_name,
        ios_version=ios_version,
        low_power=low_power,
        thermal=thermal,
    )


def make_failure_message(error_text):
    device = get_device_context()
    perm = get_location_permission_context()

    return (
        "{name} FAILED\n\n"
        "The trusted check-in phrase was received, but the phone could not get a valid location fix.\n\n"
        "Time local: {local}\n"
        "Time UTC: {utc}\n"
        "Battery: {battery}% ({battery_state})\n"
        "Location permission: {acc_auth}, {auth}\n"
        "Device: {device_model}, iOS {ios_version}\n\n"
        "Error: {error}\n\n"
        "Try calling the phone, using Apple Find My, checking existing live location sharing, "
        "or asking nearby staff/security to search the last known area."
    ).format(
        name=BEACON_NAME,
        local=iso_local(),
        utc=iso_utc(),
        battery=device.get("battery_percent", "unknown"),
        battery_state=device.get("battery_state", "unknown"),
        acc_auth=perm.get("accuracy_authorization", "unknown"),
        auth=perm.get("authorization_status", "unknown"),
        device_model=device.get("device_model", "iPhone"),
        ios_version=device.get("ios_system_version", "unknown"),
        error=error_text,
    )


def ensure_save_folder():
    root = os.path.expanduser("~/Documents")
    folder = os.path.join(root, SAVE_FOLDER_NAME)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def save_outputs(message, packet=None):
    if not SAVE_LOCAL_FILES:
        return

    try:
        folder = ensure_save_folder()
        latest_txt = os.path.join(folder, "latest_buddy_beacon_message.txt")
        with open(latest_txt, "w", encoding="utf-8") as f:
            f.write(message)

        stamp = now_local_dt().strftime("%Y%m%d_%H%M%S")
        stamped_txt = os.path.join(folder, "buddy_beacon_{}.txt".format(stamp))
        with open(stamped_txt, "w", encoding="utf-8") as f:
            f.write(message)

        if packet is not None:
            latest_json = os.path.join(folder, "latest_buddy_beacon_packet.json")
            with open(latest_json, "w", encoding="utf-8") as f:
                json.dump(packet, f, indent=2, sort_keys=True)

            stamped_json = os.path.join(folder, "buddy_beacon_{}.json".format(stamp))
            with open(stamped_json, "w", encoding="utf-8") as f:
                json.dump(packet, f, indent=2, sort_keys=True)

    except Exception:
        # Do not break the beacon just because saving failed.
        pass


def output_message(message):
    if COPY_TO_CLIPBOARD and clipboard is not None:
        try:
            clipboard.set(message)
        except Exception:
            pass

    # Critical: Shortcuts can use this printed output as "Pythonista Script Result".
    print(message)


def main():
    try:
        packet = build_packet()
        message = make_human_message(packet) if OUTPUT_HUMAN_MESSAGE else json.dumps(packet, indent=2, sort_keys=True)

        # Also include the short message in packet for AI/manual use if JSON saved.
        packet["sharing"] = {
            "short_human_message": message,
            "ai_use_note": "Prioritise find_me coordinates, rescue_search_radius_metres, timestamp, maps, location_quality, readable_place, movement, and phone_context. Do not assume coordinates are exact beyond the stated radius."
        }

        save_outputs(message, packet)
        output_message(message)

    except Exception as e:
        error_text = "{}".format(e)
        failure = make_failure_message(error_text)

        # Save traceback locally if possible.
        try:
            folder = ensure_save_folder()
            with open(os.path.join(folder, "latest_error_traceback.txt"), "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
        except Exception:
            pass

        save_outputs(failure, None)
        output_message(failure)


if __name__ == "__main__":
    main()
