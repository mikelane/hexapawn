# Hexapawn Position Solver #
**CS542  
Homework2  
Michael Lane  
24 April 2017**

#### My Approach ####

My hexapawn solver used some of the lessons I learned from my solution to the
tetrominos solver. I made good (perhaps better) use of Numpy for my hexapawn
solution. I also followed an OOP approach that seemed have paid benefits with
regard to coding time and bug prevention. 

I initially intended to make use of bitboards for this assignment. But as I was
investigating how to make that work, it occurred to me that numpy arrays could
act as if they were bitboards. For example, a pawn has two different kinds of
moves it can make: regular moves straight forward in the direction of play for
a given color and attack moves that go one diagonal to the left or right. So a
numpy array that acts like a bit mask for black pawns might look like this

    attack:     move:
    [[0 1 0]    [[0 1 0]
     [1 0 1]]    [0 1 0]]
     
The anchor point for the moves for black would be (0,1). It also occurred to me
that I would either need to add a buffer zone to the board or I would need to
add a buffer to the masks and use slices. I chose the latter. So for a 3x3
hexapawn board, the masks are actually 4x5: essentially the perimeter is 0-
padded.

When I was trying to figure out how the move generation worked, it occurred to
me that a logical AND mask would be perfect. For the regular moves, the pawns
can move into any empty space straight ahead of them. For the attacks the pawns 
can move only into spaces occupied by the opponent one diagonal to the right or
left ahead of them. So the regular move is empty spaces AND move mask anchored
at the pawn location. The attack move is opponent spaces AND anchored attack
mask. For example for the following board with the pawn at 0,0 (which is A3)
being considered:

    board:
    B
    [[p p p]
     [. P .]
     [P . P]]
     
    (sliced)           empty cell         possible
    move mask          mask               moves
    [[1 0 0]           [[0 0 0]           [[0 0 0]
     [1 0 0]     &      [1 0 1]     =      [1 0 0]
     [0 0 0]]           [0 1 0]]           [0 0 0]]
     
    (sliced)           opponent           possible
    attack mask        mask               attacks
    [[1 0 0]           [[0 0 0]           [[0 0 0]
     [0 1 0]     &      [0 1 0]     =      [0 1 0]
     [0 0 0]]           [1 0 1]]           [0 0 0]]
     
To get a list of the possible moves, I merely need to use numpy's ability to do
logical operations on arrays in exactly the way demonstrated above. Then a call
to for example `numpy.argwhere(arr == 1)` will give the list possible moves in
a list of row, col entries.

So doing, I have move generation handled. Generating the pieces that are on
move, whether or not there is a win, and any other ancillary bookkeeping is
just that simple. And since it's all compiled C under the hood, it's also very
quick. The rest was a simple matter of following the algorithm provided in
class.

#### Results ####

I used Nose to automatically generate test results (and I'll continue to do
this until I retire, because wow). I used several of my own tests for the
various internal functions and I used all of the test instances provided to us
on Moodle. All but one test passed. The failure was due to a timeout. Try as I
might, I couldn't prevent that timeout, so it'll hopefully not be an issue. The
testing outputs are as follows:

    .2017-04-23 20:36:54,913 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=6, maxsize=None, currsize=6)
    2017-04-23 20:36:54,913 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:54,913 - WARNING - hexapawn_solver - 7 Nodes :: 0.018182 seconds
     
     
    .2017-04-23 20:36:55,201 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=1, maxsize=None, currsize=1)
    2017-04-23 20:36:55,201 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:55,201 - WARNING - hexapawn_solver - 2 Nodes :: 0.004582 seconds
     
    .2017-04-23 20:36:55,600 - WARNING - hexapawn_solver - CacheInfo(hits=1, misses=22, maxsize=None, currsize=22)
    2017-04-23 20:36:55,600 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:55,600 - WARNING - hexapawn_solver - 34 Nodes :: 0.083671 seconds
     
    .2017-04-23 20:36:55,936 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=6, maxsize=None, currsize=6)
    2017-04-23 20:36:55,936 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:55,936 - WARNING - hexapawn_solver - 8 Nodes :: 0.021489 seconds
     
    .2017-04-23 20:36:56,306 - WARNING - hexapawn_solver - CacheInfo(hits=1, misses=14, maxsize=None, currsize=14)
    2017-04-23 20:36:56,306 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:56,306 - WARNING - hexapawn_solver - 23 Nodes :: 0.056047 seconds
     
    .2017-04-23 20:36:56,615 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=1, maxsize=None, currsize=1)
    2017-04-23 20:36:56,616 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:56,616 - WARNING - hexapawn_solver - 2 Nodes :: 0.004174 seconds
     
    .2017-04-23 20:36:56,950 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=8, maxsize=None, currsize=8)
    2017-04-23 20:36:56,950 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:56,950 - WARNING - hexapawn_solver - 11 Nodes :: 0.026998 seconds
     
    .2017-04-23 20:36:57,303 - WARNING - hexapawn_solver - CacheInfo(hits=1, misses=10, maxsize=None, currsize=10)
    2017-04-23 20:36:57,303 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:57,303 - WARNING - hexapawn_solver - 18 Nodes :: 0.043098 seconds
     
    .2017-04-23 20:36:57,622 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=2, maxsize=None, currsize=2)
    2017-04-23 20:36:57,622 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:57,622 - WARNING - hexapawn_solver - 2 Nodes :: 0.006235 seconds
     
    .2017-04-23 20:36:58,032 - WARNING - hexapawn_solver - CacheInfo(hits=2, misses=25, maxsize=None, currsize=25)
    2017-04-23 20:36:58,032 - WARNING - hexapawn_solver - my cache hits: 3
    2017-04-23 20:36:58,032 - WARNING - hexapawn_solver - 38 Nodes :: 0.091757 seconds
     
    .2017-04-23 20:36:58,373 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=6, maxsize=None, currsize=6)
    2017-04-23 20:36:58,373 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:58,373 - WARNING - hexapawn_solver - 7 Nodes :: 0.02144 seconds
     
    .2017-04-23 20:36:58,721 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=6, maxsize=None, currsize=6)
    2017-04-23 20:36:58,721 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:36:58,721 - WARNING - hexapawn_solver - 11 Nodes :: 0.025172 seconds
     
    .2017-04-23 20:37:02,973 - WARNING - hexapawn_solver - CacheInfo(hits=277, misses=824, maxsize=None, currsize=824)
    2017-04-23 20:37:02,973 - WARNING - hexapawn_solver - my cache hits: 16
    2017-04-23 20:37:02,973 - WARNING - hexapawn_solver - 1633 Nodes :: 3.944744 seconds
     
    .2017-04-23 20:37:03,581 - WARNING - hexapawn_solver - CacheInfo(hits=5, misses=51, maxsize=None, currsize=51)
    2017-04-23 20:37:03,581 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:03,581 - WARNING - hexapawn_solver - 86 Nodes :: 0.232565 seconds
     
    .2017-04-23 20:37:03,986 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=22, maxsize=None, currsize=22)
    2017-04-23 20:37:03,986 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:03,986 - WARNING - hexapawn_solver - 32 Nodes :: 0.08943 seconds
     
    .2017-04-23 20:37:04,305 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=1, maxsize=None, currsize=1)
    2017-04-23 20:37:04,305 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:04,305 - WARNING - hexapawn_solver - 2 Nodes :: 0.004902 seconds
     
    .2017-04-23 20:37:04,625 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=2, maxsize=None, currsize=2)
    2017-04-23 20:37:04,625 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:04,625 - WARNING - hexapawn_solver - 2 Nodes :: 0.006651 seconds
     
    .2017-04-23 20:37:04,984 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=5, maxsize=None, currsize=5)
    2017-04-23 20:37:04,984 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:04,984 - WARNING - hexapawn_solver - 8 Nodes :: 0.022806 seconds
     
    .2017-04-23 20:37:05,328 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=6, maxsize=None, currsize=6)
    2017-04-23 20:37:05,328 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:05,328 - WARNING - hexapawn_solver - 9 Nodes :: 0.028089 seconds
     
    .2017-04-23 20:37:08,317 - WARNING - hexapawn_solver - CacheInfo(hits=150, misses=543, maxsize=None, currsize=543)
    2017-04-23 20:37:08,317 - WARNING - hexapawn_solver - my cache hits: 4
    2017-04-23 20:37:08,317 - WARNING - hexapawn_solver - 1097 Nodes :: 2.656062 seconds
     
    .2017-04-23 20:37:08,662 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=1, maxsize=None, currsize=1)
    2017-04-23 20:37:08,662 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:08,662 - WARNING - hexapawn_solver - 2 Nodes :: 0.004215 seconds
     
    .2017-04-23 20:37:09,002 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=1, maxsize=None, currsize=1)
    2017-04-23 20:37:09,003 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:09,003 - WARNING - hexapawn_solver - 2 Nodes :: 0.005044 seconds
     
    .2017-04-23 20:37:09,474 - WARNING - hexapawn_solver - CacheInfo(hits=5, misses=28, maxsize=None, currsize=28)
    2017-04-23 20:37:09,474 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:09,474 - WARNING - hexapawn_solver - 45 Nodes :: 0.144566 seconds
     
    .2017-04-23 20:37:09,898 - WARNING - hexapawn_solver - CacheInfo(hits=2, misses=20, maxsize=None, currsize=20)
    2017-04-23 20:37:09,898 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:09,898 - WARNING - hexapawn_solver - 27 Nodes :: 0.090218 seconds
     
    .2017-04-23 20:37:10,239 - WARNING - hexapawn_solver - CacheInfo(hits=1, misses=8, maxsize=None, currsize=8)
    2017-04-23 20:37:10,239 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:10,239 - WARNING - hexapawn_solver - 9 Nodes :: 0.035415 seconds
     
    .2017-04-23 20:37:10,678 - WARNING - hexapawn_solver - CacheInfo(hits=1, misses=18, maxsize=None, currsize=18)
    2017-04-23 20:37:10,678 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:10,679 - WARNING - hexapawn_solver - 33 Nodes :: 0.099868 seconds
     
    .2017-04-23 20:37:11,576 - WARNING - hexapawn_solver - CacheInfo(hits=31, misses=112, maxsize=None, currsize=112)
    2017-04-23 20:37:11,576 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:11,576 - WARNING - hexapawn_solver - 191 Nodes :: 0.580336 seconds
     
    .2017-04-23 20:37:11,942 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=6, maxsize=None, currsize=6)
    2017-04-23 20:37:11,942 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:11,942 - WARNING - hexapawn_solver - 10 Nodes :: 0.031802 seconds
     
    .2017-04-23 20:37:13,235 - WARNING - hexapawn_solver - CacheInfo(hits=42, misses=189, maxsize=None, currsize=189)
    2017-04-23 20:37:13,235 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:13,235 - WARNING - hexapawn_solver - 311 Nodes :: 0.961158 seconds
     
    .2017-04-23 20:37:13,701 - WARNING - hexapawn_solver - CacheInfo(hits=2, misses=24, maxsize=None, currsize=24)
    2017-04-23 20:37:13,701 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:13,701 - WARNING - hexapawn_solver - 43 Nodes :: 0.127479 seconds
     
    .2017-04-23 20:37:17,331 - WARNING - hexapawn_solver - CacheInfo(hits=231, misses=489, maxsize=None, currsize=489)
    2017-04-23 20:37:17,331 - WARNING - hexapawn_solver - my cache hits: 1
    2017-04-23 20:37:17,331 - WARNING - hexapawn_solver - 1047 Nodes :: 3.29485 seconds
     
    .2017-04-23 20:37:35,756 - WARNING - hexapawn_solver - CacheInfo(hits=2371, misses=2487, maxsize=None, currsize=2487)
    2017-04-23 20:37:35,756 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:35,756 - WARNING - hexapawn_solver - 6184 Nodes :: 18.11224 seconds
     
    .2017-04-23 20:37:36,177 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=7, maxsize=None, currsize=7)
    2017-04-23 20:37:36,178 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:36,178 - WARNING - hexapawn_solver - 14 Nodes :: 0.044003 seconds
     
    .2017-04-23 20:37:36,515 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=5, maxsize=None, currsize=5)
    2017-04-23 20:37:36,515 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:36,515 - WARNING - hexapawn_solver - 8 Nodes :: 0.029348 seconds
     
    .2017-04-23 20:37:57,671 - WARNING - hexapawn_solver - CacheInfo(hits=2068, misses=2936, maxsize=None, currsize=2936)
    2017-04-23 20:37:57,672 - WARNING - hexapawn_solver - my cache hits: 2
    2017-04-23 20:37:57,672 - WARNING - hexapawn_solver - 7132 Nodes :: 20.848425 seconds
     
    .2017-04-23 20:37:58,080 - WARNING - hexapawn_solver - CacheInfo(hits=0, misses=4, maxsize=None, currsize=4)
    2017-04-23 20:37:58,080 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:37:58,080 - WARNING - hexapawn_solver - 7 Nodes :: 0.021437 seconds
     
    .2017-04-23 20:39:02,246 - WARNING - hexapawn_solver - CacheInfo(hits=5879, misses=8640, maxsize=None, currsize=8640)
    2017-04-23 20:39:02,246 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:39:02,246 - WARNING - hexapawn_solver - 21078 Nodes :: 63.860417 seconds

    Failure
    Traceback (most recent call last):
      File "/Users/Mike/.pyenv/versions/3.6.0/lib/python3.6/unittest/case.py", line 59, in testPartExecutor
        yield
      File "/Users/Mike/.pyenv/versions/3.6.0/lib/python3.6/unittest/case.py", line 601, in run
        testMethod()
      File "/Users/Mike/.pyenv/versions/3.6.0/lib/python3.6/site-packages/nose/case.py", line 198, in runTest
        self.test(*self.arg)
      File "/Users/Mike/.pyenv/versions/3.6.0/lib/python3.6/site-packages/nose/tools/nontrivial.py", line 100, in newfunc
        raise TimeExpired("Time limit (%s) exceeded" % limit)
    Exception: Time limit (30) exceeded


     
    F2017-04-23 20:39:05,308 - WARNING - hexapawn_solver - CacheInfo(hits=205, misses=377, maxsize=None, currsize=377)
    2017-04-23 20:39:05,308 - WARNING - hexapawn_solver - my cache hits: 0
    2017-04-23 20:39:05,308 - WARNING - hexapawn_solver - 846 Nodes :: 2.463828 seconds
     
    .2017-04-23 20:39:30,895 - WARNING - hexapawn_solver - CacheInfo(hits=2606, misses=3622, maxsize=None, currsize=3622)
    2017-04-23 20:39:30,895 - WARNING - hexapawn_solver - my cache hits: 5
    2017-04-23 20:39:30,895 - WARNING - hexapawn_solver - 8437 Nodes :: 25.264803 seconds
    .
    ======================================================================
    FAIL: tests.hexapawn_tests.test_positions('1\n', 'tests/positions/6x6-7.in')
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/Mike/.pyenv/versions/3.6.0/lib/python3.6/site-packages/nose/case.py", line 198, in runTest
        self.test(*self.arg)
      File "/Users/Mike/.pyenv/versions/3.6.0/lib/python3.6/site-packages/nose/tools/nontrivial.py", line 100, in newfunc
        raise TimeExpired("Time limit (%s) exceeded" % limit)
    nose.tools.nontrivial.TimeExpired: Time limit (30) exceeded
    -------------------- >> begin captured stdout << ---------------------
     

    --------------------- >> end captured stdout << ----------------------

    ----------------------------------------------------------------------
     
    Ran 42 tests in 156.498s

    FAILED (failures=1)