package main

import (
	"fmt"
	"math"
	"math/rand"
	"sync"
	"time"
)

const numLasers = 4

func main() {
	rand.Seed(time.Now().UnixNano())

	phaseCh := make(chan []float64)
	doneCh := make(chan bool)
	wg := &sync.WaitGroup{}

	// start monitoring and adjusting phase of each laser
	wg.Add(2)
	go monitorPhases(phaseCh, doneCh, wg)
	go adjustPhases(phaseCh, doneCh, wg)

	// wait for phase locking to complete
	<-doneCh
	wg.Wait()

	fmt.Println("Phase locking complete!")
}

func monitorPhases(phaseCh chan<- []float64, doneCh chan<- bool, wg *sync.WaitGroup) {
	defer wg.Done()

	phases := make([]float64, numLasers)
	for i := range phases {
		phases[i] = rand.Float64() * 2 * math.Pi
	}

	fmt.Println("Initial phases:", phases)

	for {
		// simulate monitoring of laser output
		time.Sleep(500 * time.Millisecond)

		// update current phases
		for i := range phases {
			phases[i] += rand.Float64()*0.1 - 0.05
			if phases[i] < 0 {
				phases[i] += 2 * math.Pi
			} else if phases[i] >= 2*math.Pi {
				phases[i] -= 2 * math.Pi
			}
		}

		// send current phases to phase adjustment goroutine
		phaseCh <- phases

		// check if phase locking is complete
		locked := true
		for _, phase := range phases {
			if phase < 0.99 || phase > 1.01 {
				locked = false
				break
			}
		}
		if locked {
			doneCh <- true
			break
		}
	}
	close(phaseCh)
}

func adjustPhases(phaseCh <-chan []float64, doneCh chan<- bool, wg *sync.WaitGroup) {
	defer wg.Done()

	phases := make([]float64, numLasers)
	copy(phases, <-phaseCh)

	for {
		// simulate adjusting phase of lasers
		time.Sleep(1 * time.Second)

		// update phase of each laser based on the monitored output
		for i := range phases {
			phases[i] += rand.Float64()*0.05 - 0.025
			if phases[i] < 0 {
				phases[i] += 2 * math.Pi
			} else if phases[i] >= 2*math.Pi {
				phases[i] -= 2 * math.Pi
			}
		}

		// print current and updated phases
		fmt.Println("Current phases:", phases)
		copy(phases, <-phaseCh)
		fmt.Println("Updated phases:", phases)

		// check if phase locking is complete
		if phases[0] > 0.99 && phases[0] < 1.01 {
			doneCh <- true
			break
		}
	}
}
