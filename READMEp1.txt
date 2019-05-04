README 
//////
CS421
University of Illinois at Chicago
Spring 2019

Omar Al-Khatib / oalkha2
Isaiah Grief / igrief2
Michael Hume / mhume3

We chose to use the CoreNLP parser interfacing with NLTK in Python. 
It seemed that the CoreNLP parser was robust and parsed sentences in a way that made displaying the parse trees easy using NLTK.
The NER tagger also seemed advantageous for the categorization task, although we did not end up using it. 
For the categorization task we used WordNet. 
The Wu-Palmer algorithm was used to calculate similarity between words.

How to run:
Have Stanford CoreNLP service up and running at http://localhost:9000 
Must have an input.txt file to pass in as an argument 
Execute with the command: oalkha2_igrief2_mhume3.py input.txt 


PARSE TREES:
(1c)
Is the Pacific deeper than the Atlantic?
(ROOT
  (SQ
    (VBZ Is)
    (NP (DT the) (NNP Pacific))
    (NP
      (NP (JJR deeper))
      (PP (IN than) (NP (DT the) (NNP Atlantic))))
    (. ?)))
                     ROOT
                      |
                      SQ
  ____________________|_______________________________
 |       |                       NP                   |
 |       |             __________|___                 |
 |       |            |              PP               |
 |       |            |      ________|___             |
 |       NP           NP    |            NP           |
 |    ___|_____       |     |         ___|_____       |
VBZ  DT       NNP    JJR    IN       DT       NNP     .
 |   |         |      |     |        |         |      |
 Is the     Pacific deeper than     the     Atlantic  ?



(1e)
Did Swank win the oscar in 2000?
(ROOT
  (SQ
    (VBD Did)
    (NP (NNP Swank))
    (VP
      (VB win)
      (NP (NP (DT the) (NN oscar)) (PP (IN in) (NP (CD 2000)))))
    (. ?)))
              ROOT
               |
               SQ
  _____________|_______________________________
 |    |                  VP                    |
 |    |     _____________|____                 |
 |    |    |                  NP               |
 |    |    |         _________|_______         |
 |    |    |        |                 PP       |
 |    |    |        |              ___|___     |
 |    NP   |        NP            |       NP   |
 |    |    |    ____|____         |       |    |
VBD  NNP   VB  DT        NN       IN      CD   .
 |    |    |   |         |        |       |    |
Did Swank win the      oscar      in     2000  ?


(1f)
Is the Shining by Kubrik?
(ROOT
  (SQ
    (VBZ Is)
    (NP (DT the))
    (NP (NP (VBG Shining)) (PP (IN by) (NP (NNP Kubrik))))
    (. ?)))
          ROOT
           |
           SQ
  _________|____________________
 |   |           NP             |
 |   |      _____|___           |
 |   |     |         PP         |
 |   |     |      ___|____      |
 |   NP    NP    |        NP    |
 |   |     |     |        |     |
VBZ  DT   VBG    IN      NNP    .
 |   |     |     |        |     |
 Is the Shining  by     Kubrik  ?

(1j)
Does the album Thriller include the track BeatIt?
(ROOT
  (S
    (VP
      (VBZ Does)
      (SBAR
        (S
          (NP (DT the) (NN album) (NN Thriller))
          (VP (VBP include) (NP (DT the) (NN track) (NN BeatIt))))))
    (. ?)))
                          ROOT
                           |
                           S
                   ________|__________________________
                  VP                                  |
  ________________|________                           |
 |                        SBAR                        |
 |                         |                          |
 |                         S                          |
 |          _______________|_________                 |
 |         |                         VP               |
 |         |                _________|____            |
 |         NP              |              NP          |
 |     ____|______         |      ________|_____      |
VBZ   DT   NN     NN      VBP    DT       NN    NN    .
 |    |    |      |        |     |        |     |     |
Does the album Thriller include the     track BeatIt  ?


(2a)
Who directed Hugo?
(ROOT
  (SBARQ
    (WHNP (WP Who))
    (SQ (VP (VBD directed) (NP (NNP Hugo))))
    (. ?)))
       ROOT
        |
      SBARQ
  ______|_______________
 |             SQ       |
 |             |        |
 |             VP       |
 |       ______|___     |
WHNP    |          NP   |
 |      |          |    |
 WP    VBD        NNP   .
 |      |          |    |
Who  directed     Hugo  ?


(2b)
Which is the scary movie by Kubrik with Nicholson?
(ROOT
  (SBARQ
    (WHNP (WDT Which))
    (SQ
      (VBZ is)
      (NP
        (NP (DT the) (JJ scary) (NN movie))
        (PP
          (IN by)
          (NP (NP (NN Kubrik)) (PP (IN with) (NP (NN Nicholson)))))))
    (. ?)))
                     ROOT
                      |
                    SBARQ
   ___________________|______________________________________
  |                   SQ                                     |
  |     ______________|____                                  |
  |    |                   NP                                |
  |    |         __________|__________                       |
  |    |        |                     PP                     |
  |    |        |           __________|___                   |
  |    |        |          |              NP                 |
  |    |        |          |     _________|____              |
  |    |        |          |    |              PP            |
  |    |        |          |    |          ____|______       |
 WHNP  |        NP         |    NP        |           NP     |
  |    |    ____|_____     |    |         |           |      |
 WDT  VBZ  DT   JJ    NN   IN   NN        IN          NN     .
  |    |   |    |     |    |    |         |           |      |
Which  is the scary movie  by Kubrik     with     Nicholson  ?



(2f)
In which continent does Canada lie?
(ROOT
  (SBARQ
    (WHPP (IN In) (WHNP (WDT which) (NN continent)))
    (SQ (VBZ does) (NP (NNP Canada)) (VP (VB lie)))
    (. ?)))
                          ROOT
                           |
                         SBARQ
       ____________________|_______________
     WHPP                        SQ        |
  ____|____                 _____|_____    |
 |        WHNP             |     NP    VP  |
 |     ____|_______        |     |     |   |
 IN  WDT           NN     VBZ   NNP    VB  .
 |    |            |       |     |     |   |
 In which      continent  does Canada lie  ?


(2h)
With which countries does France have a border?
(ROOT
  (S
    (PP
      (IN With)
      (SBAR
        (WHNP (WDT which))
        (S (NP (NNS countries)) (VP (VBZ does)))))
    (NP (NNP France))
    (VP (VB have) (NP (DT a) (NN border)))
    (. ?)))
                                   ROOT
                                    |
                                    S
             _______________________|_________________________
            PP                      |          |              |
  __________|______                 |          |              |
 |                SBAR              |          |              |
 |      ___________|______          |          |              |
 |     |                  S         |          VP             |
 |     |            ______|___      |      ____|___           |
 |    WHNP         NP         VP    NP    |        NP         |
 |     |           |          |     |     |     ___|____      |
 IN   WDT         NNS        VBZ   NNP    VB   DT       NN    .
 |     |           |          |     |     |    |        |     |
With which     countries     does France have  a      border  ?



(2m)
Where was Gaga born?
(ROOT
  (SBARQ
    (WHADVP (WRB Where))
    (SQ (VBD was) (NP (NNP Gaga)) (VP (VBN born)))
    (. ?)))
            ROOT
             |
           SBARQ
   __________|_________
  |          SQ        |
  |      ____|____     |
WHADVP  |    NP   VP   |
  |     |    |    |    |
 WRB   VBD  NNP  VBN   .
  |     |    |    |    |
Where  was  Gaga born  ?



(2n)
In which album does Aura appear?
(ROOT
  (SBARQ
    (WHPP (IN In) (WHNP (WDT which) (NN album)))
    (SQ (VBZ does) (NP (NNP Aura)) (VP (VB appear)))
    (. ?)))
                      ROOT
                       |
                     SBARQ
       ________________|________________
     WHPP                   SQ          |
  ____|____             ____|_____      |
 |        WHNP         |    NP    VP    |
 |     ____|_____      |    |     |     |
 IN  WDT         NN   VBZ  NNP    VB    .
 |    |          |     |    |     |     |
 In which      album  does Aura appear  ?



(2o)
Which album by Swift was released in 2014?
(ROOT
  (SBARQ
    (WHNP
      (WHNP (WDT Which) (NN album))
      (PP (IN by) (NP (NNP Swift))))
    (SQ (VBD was) (VP (VBN released) (PP (IN in) (NP (CD 2014)))))
    (. ?)))
                                     ROOT
                                      |
                                    SBARQ
                   ___________________|______________________________
                  |                                 SQ               |
                  |                    _____________|___             |
                 WHNP                 |                 VP           |
        __________|________           |       __________|___         |
       |                   PP         |      |              PP       |
       |                ___|____      |      |           ___|___     |
      WHNP             |        NP    |      |          |       NP   |
   ____|_____          |        |     |      |          |       |    |
 WDT         NN        IN      NNP   VBD    VBN         IN      CD   .
  |          |         |        |     |      |          |       |    |
Which      album       by     Swift  was  released      in     2014  ?
