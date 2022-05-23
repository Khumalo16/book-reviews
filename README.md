### Summary rangers
A program that produces comma delimited lists of numbers, grouping them into ranges when these lists are sequential.
In this context, a sequence is defined as two consecutive numbers with an interval of one between them. It is assumed that the input consists of sorted numbers.

## Input structure
The input contains multple test cases. The first line of the input contains the integer $N$, the number of test cases, where $ 0 < N \leqslant 2^{31}$.
This is follwed my $M$ integer $F_1, F_2,....,F_M $, where $-2^{31}\leqslant F_i \leqslant 2^{31}$. The integers are seperated by a single comma. An empty line is ignored in the input.
    

## Output structure
For each input case, the output must start with a line that contains the case number $(1,2,3...)$, followed immediately by a colon, a single space and then list of delemited integers.The answer in the output appears the same order as they appear in the input.

## Suggested output structure
As previously explained (Output structure), the suggested output follows the same structure. The name of the suggested output must match the name of the input and the extension file should end with ***.suggested***, i.e ***testName.suggested***

***Note: The end of the content should be a single new line without a leading white space (See suggested output examples in the testcases folder)***

## How to run the program
Extract impact.zip file. Open the extract folder. You can run the program manual or run with provided script file.

# Run manual
    Open terminal and navigate to the extracted impact directory and excecute the followeing command:
        javac numberrangesummarizer/*.java 
        java numberrangesummarizer.Main<testcases/testName.txt
where __testName__ is the name of the test case

# Run with testcases
    Similarily, open terminal and navigete to the impact directory 
    and use the provided ***rushtests.sh*** srcipt file as follows (This script is designed for Linux users):
        ./runtests.sh

***Note: If You wish to include more testcases, include them in the testcases folder as well as their corresponding suggested output***

# Libraries
    Imported library includes:
        java.util.ArrayList
        java.util.Collection
        java.util.Iterator
        java.io.BufferedReader
        java.io.IOException
        java.io.InputStreeamReader
        
No extenal libraies used for this program.
    

    

