package wordcount

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"reflect"
	"regexp"
	"strings"
	"time"

	"github.com/apache/beam/sdks/v2/go/pkg/beam"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/x/beamx"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/core/graph/mtime"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/core/graph/window"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/io/textio"
	"github.com/apache/beam/sdks/v2/go/pkg/beam/transforms/stats"

	_ "github.com/apache/beam/sdks/v2/go/pkg/beam/io/filesystem/local"
)

func init() {
	beam.RegisterFunction(formatFn)
	beam.RegisterType(reflect.TypeOf((*eventProcessingTime)(nil)).Elem())
}

// formatFn is a DoFn that formats a windowed word and its count as a string.
// func Unix(sec int64, nsec int64) Time
func formatFn(iw beam.Window, et beam.EventTime, w string, c int) string {
	t := time.Unix(0, et.Milliseconds() * int64(time.Millisecond)).Format(time.RFC1123)
	s := fmt.Sprintf("%s@%v %s: %v", t, iw, w, c)
	return s
}

var stopWords []string = []string{"a", "and", "but", "he", "her", "hers", "him", "his", "if", "is", "it", 
				"or", "the", "that", "there", "then", "they", "them",
		 		"this", "was", "where", "when", "which", "who", "whom"}

// The incoming string messages will be assigned a random timestamp somewhere in a
// 2-hour period
type eventProcessingTime struct {
	Min beam.EventTime `json:"min"`
}
// Contains a non-negative pseudo-random number in [0, n) of 63-bit integer n as an int64 type
func (f *eventProcessingTime) ProcessElement(x beam.X) (beam.EventTime, beam.X) {
	timestamp := f.Min.Add(time.Duration(rand.Int63n(2 * time.Hour.Nanoseconds())))
	return timestamp, x
}

type Pipeline struct {
	pipe  *beam.Pipeline
  	scope beam.Scope
}

func CreatePipeline() *Pipeline {
        beam.Init()
        p := beam.NewPipeline()
        pipe := Pipeline {
                pipe: p,
                scope: p.Root(),
        }
	return &pipe
}

func (pipe *Pipeline) Process(input []interface{}, outputFile string){
// Returns a PCollection of type string (i.e. each line from the text)
        lines := beam.Create(pipe.scope, input...)

// Add an element timestamp
	tsLines := beam.ParDo(pipe.scope, &eventProcessingTime{Min: mtime.Now()}, lines)

// For sliding windows
//        wndLines := beam.WindowInto(
//			pipe.scope, 
//			window.NewSlidingWindows(5 * time.Minute, 30 * time.Minute), 
//			tsLines)
// Add fixed windowing
      wndLines := beam.WindowInto(pipe.scope, window.NewFixedWindows(30 * time.Minute), tsLines)

// Returns a PCollection of of type string
// Inline DoFn using an anonymous function
	var re = regexp.MustCompile(`[a-zA-Z]+('[a-z])?`)
	words := beam.ParDo(pipe.scope, func(line string, emit func(string)) {
		for _, word := range re.FindAllString(line, -1) {
			var contains bool
			for _, w := range stopWords {
				contains = strings.EqualFold(w, word)
				if contains {
					break
				}
			}
			if !(contains) {
				emit(word)
			}
		}
	}, wndLines)

// Returns a PCollection of type <K, V>
	counted := stats.Count(pipe.scope, words)

	formatted := beam.ParDo(pipe.scope, formatFn, counted)

// textio.Write does not support windowed writes, so we
// simply include the window in the output and re-window back into the global window
// before the write.
	merged := beam.WindowInto(pipe.scope, window.NewGlobalWindows(), formatted)

	textio.Write(pipe.scope, outputFile, merged)

// Run the pipeline on the direct runner.
// Background() returns a non-nil empty context that is never cancelled
	if err := beamx.Run(context.Background(), pipe.pipe); err != nil {
		log.Fatalf("Failed to execute job: %v", err)
	}
}
