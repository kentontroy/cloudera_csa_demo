package main

import (
        "flag"
        w "pse.cloudera.com/wordcount"
)

func main(){
        input := []interface{}{"Jon Snow", "Jaime Lannister", "The Night King",
                        "Tyrion Lannister", "Cersei Lannister"}

        var outputFile string
        flag.StringVar(&outputFile, "outputFile", "foo.out", "File to output")
        flag.Parse()

        pipe := w.CreatePipeline()
        pipe.Process(input, outputFile)
}
