import math
from typing import Tuple

def direction(lonOrigin: float, latOrigin: float, 
              lonDest:   float, latDest:   float) -> Tuple[str, float]:
  compass = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
  deltaLon = lonDest - lonOrigin
  deltaLat = latDest - latOrigin
  degrees = math.atan2(deltaLon, deltaLat) / math.pi * 180 
  if degrees < 0:  
    degrees = degrees + 360 
  return compass[round(degrees / 45)], degrees

def main():
  print(direction(2, 3, -2, -1))

if __name__ == "__main__":
  main()

