// Usage: go run radiation.go  |  go run radiation.go bench N
package main

import (
	"fmt"
	"os"
	"strconv"
)

const sigma = 5.670374419e-8

func flux(e, t, ts float64) float64 { t2, s2 := t*t, ts*ts; return e * sigma * (t2*t2 - s2*s2) }

func main() {
	if len(os.Args) > 2 && os.Args[1] == "bench" {
		n, _ := strconv.Atoi(os.Args[2])
		s := 0.0
		for i := 0; i < n; i++ {
			s += flux(0.8, 300+float64(i%900), 300)
		}
		fmt.Printf("checksum,%.6e\n", s)
		return
	}
	for t := 400; t <= 1200; t += 200 {
		fmt.Printf("%d,%.3f\n", t, flux(0.8, float64(t), 300))
	}
}
