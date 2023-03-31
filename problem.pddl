(define (problem p01)
(:domain bookWorld)
(:objects
tbot3 - robot
tbot3_init_loc - location
book_1 book_2 book_3 book_4 book_5 book_6 book_7 book_8 - book
bin_1 bin_2 bin_3 bin_4 - bin
book_1_iloc book_2_iloc book_3_iloc book_4_iloc book_5_iloc book_6_iloc book_7_iloc book_8_iloc - location
bin_1_iloc bin_2_iloc bin_3_iloc bin_4_iloc - location
artificial_intelligence operating_systems_architecture - subject
small large - size
)
(:init
(Book_At book_1 book_1_iloc)
(Book_At book_2 book_2_iloc)
(Book_At book_3 book_3_iloc)
(Book_At book_4 book_4_iloc)
(Book_At book_5 book_5_iloc)
(Book_At book_6 book_6_iloc)
(Book_At book_7 book_7_iloc)
(Book_At book_8 book_8_iloc)
(Bin_At bin_1 bin_1_iloc)
(Bin_At bin_2 bin_2_iloc)
(Bin_At bin_3 bin_3_iloc)
(Bin_At bin_4 bin_4_iloc)
(Book_Subject book_1 operating_systems_architecture)
(Book_Size book_1 small)
(Book_Subject book_2 operating_systems_architecture)
(Book_Size book_2 large)
(Book_Subject book_3 operating_systems_architecture)
(Book_Size book_3 small)
(Book_Subject book_4 operating_systems_architecture)
(Book_Size book_4 large)
(Book_Subject book_5 artificial_intelligence)
(Book_Size book_5 small)
(Book_Subject book_6 artificial_intelligence)
(Book_Size book_6 large)
(Book_Subject book_7 artificial_intelligence)
(Book_Size book_7 small)
(Book_Subject book_8 artificial_intelligence)
(Book_Size book_8 large)
(Bin_Subject bin_1 operating_systems_architecture)
(Bin_Size bin_1 small)
(Bin_Subject bin_2 operating_systems_architecture)
(Bin_Size bin_2 large)
(Bin_Subject bin_3 artificial_intelligence)
(Bin_Size bin_3 small)
(Bin_Subject bin_4 artificial_intelligence)
(Bin_Size bin_4 large)
(Robot_At tbot3 tbot3_init_loc)
(Empty_Basket tbot3)
)
(:goal (and (forall (?B - book) (exists (?BIN - bin ?L - location ?S - size ?SJ - subject) (and (Bin_At ?BIN ?L) (Book_Subject ?B ?SJ) (Book_Size ?B ?S) (Bin_Subject ?BIN ?SJ) (Bin_Size ?BIN ?S) (Book_At ?B ?L))))))
)