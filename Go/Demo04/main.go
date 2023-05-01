package main

import (
    "fmt"
    "math"
    "sync"
    "time"
	"math/rand"
)

const (
    numLasers       = 4
    maxPhase        = math.Pi
    maxPhaseStep    = math.Pi / 10
    lockThreshold   = 0.1
    correctionSpeed = 0.01
)

var (
    lasers     [numLasers]float64
    phases     [numLasers]float64
    phaseSteps [numLasers]float64
    lockStatus [numLasers]bool
)

func main() {
    var wg sync.WaitGroup
    wg.Add(numLasers)

    // initialize phases randomly
    for i := 0; i < numLasers; i++ {
        phases[i] = randPhase()
        phaseSteps[i] = maxPhaseStep
        lockStatus[i] = false
    }

    go func() {
        for {
            time.Sleep(100 * time.Millisecond)
            fmt.Println("\nPhases:", phases)
            fmt.Println("Lock Status:", lockStatus)
        }
    }()

    for i := 0; i < numLasers; i++ {
        go func(laserIndex int) {
            defer wg.Done()

            for {
                // simulate laser output
                lasers[laserIndex] = math.Sin(phases[laserIndex])

                // calculate phase error
                var phaseError float64
                for j := 0; j < numLasers; j++ {
                    if j != laserIndex {
                        phaseError += math.Sin(phases[j] - phases[laserIndex])
                    }
                }

                // adjust phase
                phaseSteps[laserIndex] += correctionSpeed * phaseError
                if phaseSteps[laserIndex] > maxPhaseStep {
                    phaseSteps[laserIndex] = maxPhaseStep
                } else if phaseSteps[laserIndex] < -maxPhaseStep {
                    phaseSteps[laserIndex] = -maxPhaseStep
                }
                phases[laserIndex] += phaseSteps[laserIndex]

                // check lock status
                lockStatus[laserIndex] = false
                for j := 0; j < numLasers; j++ {
                    if j != laserIndex {
                        if math.Abs(phases[j]-phases[laserIndex]) < lockThreshold {
                            lockStatus[laserIndex] = true
                            break
                        }
                    }
                }

                time.Sleep(1 * time.Millisecond)
            }
        }(i)
    }

    wg.Wait()
}

func randPhase() float64 {
    return 2 * math.Pi * rand.Float64()
}
