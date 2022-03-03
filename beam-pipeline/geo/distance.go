package main

import (
	"flag"
	"fmt"
	"math"
)

func main(){
	var lat1, lon1, lat2, lon2 float64
        flag.Float64Var(&lat1, "lat1", 0.0, "Latitude 1")
        flag.Float64Var(&lon1, "lon1", 0.0, "Longitude 1")
        flag.Float64Var(&lat2, "lat2", 0.0, "Latitude 2")
        flag.Float64Var(&lon2, "lon2", 0.0, "Longitude 2")
        flag.Parse()

 	km, miles := getHaversineDist(lon1, lat1, lon2, lat2) 	
        s := fmt.Sprintf("Dist %f kilometers, %f miles", km, miles) 
	fmt.Println(s)
}

func getHaversineDist(lon1, lat1, lon2, lat2 float64) (km float64, miles float64) {
	const earthRadius float64 = 6371 // Radius of the earth in km

	dLon := (lon2 - lon1) * (math.Pi / 180)
	dLat := (lat2 - lat1) * (math.Pi / 180)

  	a := math.Pow(math.Sin(dLat / 2), 2) +
    		math.Cos(lat1 * (math.Pi / 180)) * 
		math.Cos(lat2 * (math.Pi / 180)) * 
    		math.Sin(dLon / 2) * math.Sin(dLon / 2)
     
  	c := 2 * math.Atan2(math.Sqrt(a), math.Sqrt(1 - a))

  	km = earthRadius * c 
  	miles = km / 1.609344 
	return km, miles
}
