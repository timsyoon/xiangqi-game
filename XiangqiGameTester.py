# Author: Timothy Yoon
# Date of Original Submission: March 10, 2020
# Description: This test file tests the various classes in XiangqiGame.py.

import unittest
from XiangqiGame import XiangqiGame, Board, Point, Piece, General, Advisor, \
    Elephant, Horse, Chariot, Cannon, Soldier


class TestXiangqiGame(unittest.TestCase):
    """
    Test all the classes in XiangqiGame.py.
    """
    def test_1(self):   # passed
        """
        Test whether the board prints correctly.
        """
        game = XiangqiGame()
        game.print_board()

    def test_2a(self):   # passed
        """
        Test whether XiangqiGame has been initialized properly.
        """
        game = XiangqiGame()
        print(game.get_game_state())
        print(game.is_in_check("red"))
        print(game.is_in_check("black"))
        print(game.get_whose_turn())

        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertEqual(game.is_in_check("red"), False)
        self.assertEqual(game.is_in_check("black"), False)
        self.assertEqual(game.get_whose_turn(), "red")

    def test_2b(self):   # passed
        """
        Test whether XiangqiGame's setter methods are functional.
        """
        game = XiangqiGame()

        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertEqual(game.is_in_check("red"), False)
        self.assertEqual(game.is_in_check("black"), False)
        self.assertEqual(game.get_whose_turn(), "red")

        game.set_game_state("RED_WON")
        game.set_whose_turn("black")

        self.assertEqual(game.get_game_state(), "RED_WON")
        self.assertEqual(game.get_whose_turn(), "black")

        game.remove_from_check("red")
        game.remove_from_check("black")
        game.set_whose_turn("red")

        self.assertEqual(game.is_in_check("red"), False)
        self.assertEqual(game.is_in_check("black"), False)
        self.assertEqual(game.get_whose_turn(), "red")


    def test_3(self):   # passed
        """
        Test whether quantify_location works correctly.
        """
        game = XiangqiGame()
        game.print_board()
        self.assertEqual(game.quantify_location("a1"), (1, 1))
        self.assertEqual(game.quantify_location("b9"), (2, 9))
        self.assertEqual(game.quantify_location("c2"), (3, 2))
        self.assertEqual(game.quantify_location("d5"), (4, 5))
        self.assertEqual(game.quantify_location("e6"), (5, 6))
        self.assertEqual(game.quantify_location("f10"), (6, 10))
        self.assertEqual(game.quantify_location("g4"), (7, 4))
        self.assertEqual(game.quantify_location("h3"), (8, 3))
        self.assertEqual(game.quantify_location("i8"), (9, 8))

    def test_4(self):   # passed
        """
        Test if XiangqiGame's make_move() returns False if the point being
        moved from is empty.
        """
        game = XiangqiGame()
        game.print_board()

        self.assertEqual(game.make_move("a2", "a3"), False)
        self.assertEqual(game.make_move("a9", "b9"), False)
        self.assertEqual(game.make_move("i5", "i6"), False)
        self.assertEqual(game.make_move("e8", "f6"), False)

    def test_5(self):   # passed
        """
        Test if XiangqiGame's make_move() returns False if the point being
        moved from does not contain a piece belonging to the player whose turn
        it is.
        """
        game = XiangqiGame()
        game.print_board()
        self.assertEqual(game.get_whose_turn(), "red")

        self.assertEqual(game.make_move("a10", "a8"), False)
        self.assertEqual(game.make_move("b10", "a8"), False)
        self.assertEqual(game.make_move("c10", "e8"), False)
        self.assertEqual(game.make_move("d10", "c9"), False)
        self.assertEqual(game.make_move("e10", "e9"), False)
        self.assertEqual(game.make_move("f10", "e9"), False)
        self.assertEqual(game.make_move("g10", "i8"), False)
        self.assertEqual(game.make_move("h10", "i8"), False)
        self.assertEqual(game.make_move("i10", "i8"), False)
        self.assertEqual(game.make_move("b8", "b1"), False)
        self.assertEqual(game.make_move("h8", "h1"), False)
        self.assertEqual(game.make_move("a7", "a6"), False)
        self.assertEqual(game.make_move("c7", "c6"), False)
        self.assertEqual(game.make_move("e7", "e6"), False)
        self.assertEqual(game.make_move("g7", "g6"), False)
        self.assertEqual(game.make_move("i7", "i6"), False)

        game.set_whose_turn("black")
        self.assertEqual(game.get_whose_turn(), "black")

        self.assertEqual(game.make_move("a1", "a2"), False)
        self.assertEqual(game.make_move("b1", "c3"), False)
        self.assertEqual(game.make_move("c1", "e3"), False)
        self.assertEqual(game.make_move("d1", "e2"), False)
        self.assertEqual(game.make_move("e1", "e2"), False)
        self.assertEqual(game.make_move("f1", "e2"), False)
        self.assertEqual(game.make_move("g1", "i3"), False)
        self.assertEqual(game.make_move("h1", "i3"), False)
        self.assertEqual(game.make_move("i1", "i2"), False)
        self.assertEqual(game.make_move("b3", "b10"), False)
        self.assertEqual(game.make_move("h3", "h10"), False)
        self.assertEqual(game.make_move("a4", "a5"), False)
        self.assertEqual(game.make_move("c4", "c5"), False)
        self.assertEqual(game.make_move("e4", "e5"), False)
        self.assertEqual(game.make_move("g4", "g5"), False)
        self.assertEqual(game.make_move("i4", "i5"), False)

    def test_6(self):   # passed
        """
        Test XiangqiGame's make_move(). If the point moved to has a piece
        owned by the player whose turn it is, return False.
        """
        game = XiangqiGame()
        game.print_board()
        self.assertEqual(game.get_whose_turn(), "red")

        self.assertEqual(game.make_move("a1", "a4"), False)
        self.assertEqual(game.make_move("d1", "e4"), False)
        self.assertEqual(game.make_move("i1", "i4"), False)
        self.assertEqual(game.make_move("g4", "b3"), False)

        game.set_whose_turn("black")
        self.assertEqual(game.make_move("a10", "a7"), False)
        self.assertEqual(game.make_move("i10", "i7"), False)
        self.assertEqual(game.make_move("b10", "i7"), False)
        self.assertEqual(game.make_move("h10", "g7"), False)
        self.assertEqual(game.make_move("c7", "d10"), False)

    def test_7(self):   # passed
        """
        Test XiangqiGame's make_move(). If the game has already been won,
        return False.
        """
        game = XiangqiGame()
        game.print_board()
        game.set_game_state("BLACK_WON")   # Currently red's turn
        self.assertEqual(game.make_move('e1', 'e2'), False)

        game_1 = XiangqiGame()
        game_1.set_game_state("RED_WON")
        game_1.set_whose_turn("black")     # Now black's turn
        self.assertEqual(game_1.make_move('i10', 'i9'), False)

    def test_8(self):   # passed
        """
        Test whether the pieces have been initialized properly.
        """
        game = XiangqiGame()
        game.print_board()

        board = game._board.get_board()

        # Check red side
        self.assertTrue(isinstance(board[(1, 1)].get_contains(), Chariot))
        self.assertEqual(board[(1, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(1, 1)].get_contains().get_col(), 1)
        self.assertEqual(board[(1, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(2, 1)].get_contains(), Horse))
        self.assertEqual(board[(2, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(2, 1)].get_contains().get_col(), 2)
        self.assertEqual(board[(2, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(3, 1)].get_contains(), Elephant))
        self.assertEqual(board[(3, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(3, 1)].get_contains().get_col(), 3)
        self.assertEqual(board[(3, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(4, 1)].get_contains(), Advisor))
        self.assertEqual(board[(4, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(4, 1)].get_contains().get_col(), 4)
        self.assertEqual(board[(4, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(5, 1)].get_contains(), General))
        self.assertEqual(board[(5, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(5, 1)].get_contains().get_col(), 5)
        self.assertEqual(board[(5, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(6, 1)].get_contains(), Advisor))
        self.assertEqual(board[(6, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(6, 1)].get_contains().get_col(), 6)
        self.assertEqual(board[(6, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(7, 1)].get_contains(), Elephant))
        self.assertEqual(board[(7, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(7, 1)].get_contains().get_col(), 7)
        self.assertEqual(board[(7, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(8, 1)].get_contains(), Horse))
        self.assertEqual(board[(8, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(8, 1)].get_contains().get_col(), 8)
        self.assertEqual(board[(8, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(9, 1)].get_contains(), Chariot))
        self.assertEqual(board[(9, 1)].get_contains().get_color(), "red")
        self.assertEqual(board[(9, 1)].get_contains().get_col(), 9)
        self.assertEqual(board[(9, 1)].get_contains().get_row(), 1)

        self.assertTrue(isinstance(board[(2, 3)].get_contains(), Cannon))
        self.assertEqual(board[(2, 3)].get_contains().get_color(), "red")
        self.assertEqual(board[(2, 3)].get_contains().get_col(), 2)
        self.assertEqual(board[(2, 3)].get_contains().get_row(), 3)

        self.assertTrue(isinstance(board[(8, 3)].get_contains(), Cannon))
        self.assertEqual(board[(8, 3)].get_contains().get_color(), "red")
        self.assertEqual(board[(8, 3)].get_contains().get_col(), 8)
        self.assertEqual(board[(8, 3)].get_contains().get_row(), 3)

        self.assertTrue(isinstance(board[(1, 4)].get_contains(), Soldier))
        self.assertEqual(board[(1, 4)].get_contains().get_color(), "red")
        self.assertEqual(board[(1, 4)].get_contains().get_col(), 1)
        self.assertEqual(board[(1, 4)].get_contains().get_row(), 4)

        self.assertTrue(isinstance(board[(3, 4)].get_contains(), Soldier))
        self.assertEqual(board[(3, 4)].get_contains().get_color(), "red")
        self.assertEqual(board[(3, 4)].get_contains().get_col(), 3)
        self.assertEqual(board[(3, 4)].get_contains().get_row(), 4)

        self.assertTrue(isinstance(board[(5, 4)].get_contains(), Soldier))
        self.assertEqual(board[(5, 4)].get_contains().get_color(), "red")
        self.assertEqual(board[(5, 4)].get_contains().get_col(), 5)
        self.assertEqual(board[(5, 4)].get_contains().get_row(), 4)

        self.assertTrue(isinstance(board[(7, 4)].get_contains(), Soldier))
        self.assertEqual(board[(7, 4)].get_contains().get_color(), "red")
        self.assertEqual(board[(7, 4)].get_contains().get_col(), 7)
        self.assertEqual(board[(7, 4)].get_contains().get_row(), 4)

        self.assertTrue(isinstance(board[(9, 4)].get_contains(), Soldier))
        self.assertEqual(board[(9, 4)].get_contains().get_color(), "red")
        self.assertEqual(board[(9, 4)].get_contains().get_col(), 9)
        self.assertEqual(board[(9, 4)].get_contains().get_row(), 4)

        # Check black side
        self.assertTrue(isinstance(board[(1, 10)].get_contains(), Chariot))
        self.assertEqual(board[(1, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(1, 10)].get_contains().get_col(), 1)
        self.assertEqual(board[(1, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(2, 10)].get_contains(), Horse))
        self.assertEqual(board[(2, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(2, 10)].get_contains().get_col(), 2)
        self.assertEqual(board[(2, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(3, 10)].get_contains(), Elephant))
        self.assertEqual(board[(3, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(3, 10)].get_contains().get_col(), 3)
        self.assertEqual(board[(3, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(4, 10)].get_contains(), Advisor))
        self.assertEqual(board[(4, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(4, 10)].get_contains().get_col(), 4)
        self.assertEqual(board[(4, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(5, 10)].get_contains(), General))
        self.assertEqual(board[(5, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(5, 10)].get_contains().get_col(), 5)
        self.assertEqual(board[(5, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(6, 10)].get_contains(), Advisor))
        self.assertEqual(board[(6, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(6, 10)].get_contains().get_col(), 6)
        self.assertEqual(board[(6, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(7, 10)].get_contains(), Elephant))
        self.assertEqual(board[(7, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(7, 10)].get_contains().get_col(), 7)
        self.assertEqual(board[(7, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(8, 10)].get_contains(), Horse))
        self.assertEqual(board[(8, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(8, 10)].get_contains().get_col(), 8)
        self.assertEqual(board[(8, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(9, 10)].get_contains(), Chariot))
        self.assertEqual(board[(9, 10)].get_contains().get_color(), "black")
        self.assertEqual(board[(9, 10)].get_contains().get_col(), 9)
        self.assertEqual(board[(9, 10)].get_contains().get_row(), 10)

        self.assertTrue(isinstance(board[(2, 8)].get_contains(), Cannon))
        self.assertEqual(board[(2, 8)].get_contains().get_color(), "black")
        self.assertEqual(board[(2, 8)].get_contains().get_col(), 2)
        self.assertEqual(board[(2, 8)].get_contains().get_row(), 8)

        self.assertTrue(isinstance(board[(8, 8)].get_contains(), Cannon))
        self.assertEqual(board[(8, 8)].get_contains().get_color(), "black")
        self.assertEqual(board[(8, 8)].get_contains().get_col(), 8)
        self.assertEqual(board[(8, 8)].get_contains().get_row(), 8)

        self.assertTrue(isinstance(board[(1, 7)].get_contains(), Soldier))
        self.assertEqual(board[(1, 7)].get_contains().get_color(), "black")
        self.assertEqual(board[(1, 7)].get_contains().get_col(), 1)
        self.assertEqual(board[(1, 7)].get_contains().get_row(), 7)

        self.assertTrue(isinstance(board[(3, 7)].get_contains(), Soldier))
        self.assertEqual(board[(3, 7)].get_contains().get_color(), "black")
        self.assertEqual(board[(3, 7)].get_contains().get_col(), 3)
        self.assertEqual(board[(3, 7)].get_contains().get_row(), 7)

        self.assertTrue(isinstance(board[(5, 7)].get_contains(), Soldier))
        self.assertEqual(board[(5, 7)].get_contains().get_color(), "black")
        self.assertEqual(board[(5, 7)].get_contains().get_col(), 5)
        self.assertEqual(board[(5, 7)].get_contains().get_row(), 7)

        self.assertTrue(isinstance(board[(7, 7)].get_contains(), Soldier))
        self.assertEqual(board[(7, 7)].get_contains().get_color(), "black")
        self.assertEqual(board[(7, 7)].get_contains().get_col(), 7)
        self.assertEqual(board[(7, 7)].get_contains().get_row(), 7)

        self.assertTrue(isinstance(board[(9, 7)].get_contains(), Soldier))
        self.assertEqual(board[(9, 7)].get_contains().get_color(), "black")
        self.assertEqual(board[(9, 7)].get_contains().get_col(), 9)
        self.assertEqual(board[(9, 7)].get_contains().get_row(), 7)

    def test_9(self):   # passed
        """
        Test whether the generals' shadows are correct.
        """
        game = XiangqiGame()
        game.print_board()
        board = game._board.get_board()

        self.assertEqual(board[5,1].get_contains().get_shadows(), [(5,2)])
        self.assertEqual(board[5,10].get_contains().get_shadows(), [(5,9)])

    def test_10(self):   # passed
        """
        Test whether the advisors' shadows are correct.
        """
        game = XiangqiGame()
        game.print_board()
        board = game._board.get_board()

        # Test the red advisors
        self.assertEqual(board[4,1].get_contains().get_shadows(),
                         [(5,2)])

        self.assertEqual(board[6,1].get_contains().get_shadows(),
                         [(5,2)])

        # Test the black advisors
        self.assertEqual(board[4,10].get_contains().get_shadows(),
                         [(5,9)])

        self.assertEqual(board[6,10].get_contains().get_shadows(),
                         [(5,9)])

    def test_11(self):   # passed
        """
        Test whether the elephants' shadows are correct.
        """
        game = XiangqiGame()
        game.print_board()
        board = game._board.get_board()

        # Test the red elephants
        self.assertEqual(board[3,1].get_contains().get_shadows(),
                         [(5,3), (1,3)])

        self.assertEqual(board[7,1].get_contains().get_shadows(),
                         [(9,3), (5,3)])

        # Test the black elephants
        self.assertEqual(board[3,10].get_contains().get_shadows(),
                         [(5,8), (1,8)])

        self.assertEqual(board[7,10].get_contains().get_shadows(),
                         [(9,8), (5,8)])

    def test_12(self):   # passed
        """
        Test whether the horses' shadows are correct.
        """
        game = XiangqiGame()
        game.print_board()
        board = game._board.get_board()

        # Test the red horses
        self.assertEqual(board[2,1].get_contains().get_shadows(),
                         [(3,3), (1,3)])

        self.assertEqual(board[8,1].get_contains().get_shadows(),
                         [(9,3), (7,3)])

        # Test the black horses
        self.assertEqual(board[2,10].get_contains().get_shadows(),
                         [(1,8), (3,8)])

        self.assertEqual(board[8,10].get_contains().get_shadows(),
                         [(7,8), (9,8)])

    def test_13(self):   # passed
        """
        Test whether the chariots' shadows are correct.
        """
        game = XiangqiGame()
        game.print_board()
        board = game._board.get_board()

        # Test the red chariots
        self.assertEqual(board[1,1].get_contains().get_shadows(),
                         [(1,2), (1,3)])

        self.assertEqual(board[9,1].get_contains().get_shadows(),
                         [(9,2), (9,3)])

        # Test the black chariots
        self.assertEqual(board[1,10].get_contains().get_shadows(),
                         [(1,9), (1,8)])

        self.assertEqual(board[9,10].get_contains().get_shadows(),
                         [(9,9), (9,8)])

    def test_14(self):   # passed
        """
        Test whether the cannons' shadows are correct.
        """
        game = XiangqiGame()
        game.print_board()
        board = game._board.get_board()

        # Test the red cannons
        self.assertEqual(board[(2,3)].get_contains().get_shadows(),
                         [(2,2), (2,4), (2,5), (2,6), (2,7), (2,10), (3,3),
                          (4,3), (5,3), (6,3), (7,3), (1,3)])

        self.assertEqual(board[(8,3)].get_contains().get_shadows(),
                         [(8,2), (8,4), (8,5), (8,6), (8,7), (8,10), (9,3),
                         (7,3), (6,3), (5,3), (4,3), (3,3)])

        # Test the black cannons
        self.assertEqual(board[(2,8)].get_contains().get_shadows(),
                         [(2,7), (2,6), (2,5), (2,4), (2,1), (2,9), (3,8),
                          (4,8), (5,8), (6,8), (7,8), (1,8)])

        self.assertEqual(board[(8,8)].get_contains().get_shadows(),
                         [(8,7), (8,6), (8,5), (8,4), (8,1), (8,9), (9,8),
                          (7,8), (6,8), (5,8), (4,8), (3,8)])

    def test_15(self):   # passed
        """
        Test whether the soldiers' shadows are correct.
        """
        game = XiangqiGame()
        game.print_board()
        board = game._board.get_board()

        # Test the red soldiers
        self.assertEqual(board[(1,4)].get_contains().get_shadows(), [(1,5)])
        self.assertEqual(board[(3,4)].get_contains().get_shadows(), [(3,5)])
        self.assertEqual(board[(5,4)].get_contains().get_shadows(), [(5,5)])
        self.assertEqual(board[(7,4)].get_contains().get_shadows(), [(7,5)])
        self.assertEqual(board[(9,4)].get_contains().get_shadows(), [(9,5)])

        # Test the black soldiers
        self.assertEqual(board[(1,7)].get_contains().get_shadows(), [(1,6)])
        self.assertEqual(board[(3,7)].get_contains().get_shadows(), [(3,6)])
        self.assertEqual(board[(5,7)].get_contains().get_shadows(), [(5,6)])
        self.assertEqual(board[(7,7)].get_contains().get_shadows(), [(7,6)])
        self.assertEqual(board[(9,7)].get_contains().get_shadows(), [(9,6)])


    def test_16(self):   # passed
        """
        Test whether print_pieces_shadows and print_points_shadows work.
        """
        game = XiangqiGame()
        game.print_board()
        game.get_game_board().print_pieces_shadows()
        game.get_game_board().print_points_shadows()

    def test_17(self):   # passed
        """
        Test make_move for the red and black general. Test whether the
        "flying general" condition can be activated.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('e1', 'e2')  # Red move
        print("e1-e2")
        game.print_board()

        game.get_game_board().print_pieces_shadows()  #
        game.get_game_board().print_points_shadows()  #

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

    def test_18(self):   # passed
        """
        Test make_move for the red and black soldier. Test normal movement
        before the river is crossed and enhanced movement after it is crossed.
        """
        game = XiangqiGame()
        board = game.get_game_board().get_board()
        game.print_board()
        move_1 = game.make_move('a4', 'a5')  # Red move
        print("a4-a5")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('a7', 'a6')  # Black move
        print("a7-a6")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_3 = game.make_move('a5', 'a6')  # Red move
        print("a5-a6")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_4 = game.make_move('i7', 'i6')  # Black move
        print("i7-i6")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_5 = game.make_move('c4', 'c5')  # Red move
        print("c4-c5")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_6 = game.make_move('i6', 'i5')  # Black move
        print("i6-i5")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_7 = game.make_move('c5', 'c6')  # Red move
        print("c5-c6")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_8 = game.make_move('i5', 'i4')  # Black move
        print("i5-i4")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_9 = game.make_move('c6', 'c7')  # Red move
        print("c6-c7")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_10 = game.make_move('e7', 'e6')  # Black move
        print("e7-e6")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_11 = game.make_move('c7', 'b7')  # Red move
        print("c7-b7")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_12 = game.make_move('e6', 'e5')  # Black move
        print("e6-e5")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_13 = game.make_move('b7', 'b8')  # Red move
        print("b7-b8")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_13)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_14 = game.make_move('e5', 'e4')  # Black move
        print("e5-e4")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_14)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

    def test_19(self):   # passed
        """
        Test make_move for the red and black advisors.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('d1', 'e2')  # Red move
        print("d1-e2")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('d10', 'e9')  # Black move
        print("d10-e9")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_3 = game.make_move('e2', 'f3')  # Red move
        print("e2-f3")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_4 = game.make_move('e9', 'f8')  # Black move
        print("e9-f8")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_5 = game.make_move('f1', 'e2')  # Red move
        print("f1-e2")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_6 = game.make_move('f10', 'e9')  # Black move
        print("f10-e9")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_7 = game.make_move('e2', 'd3')  # Red move
        print("e2-d3")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_8 = game.make_move('e9', 'd8')  # Black move
        print("e9-d8")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_9 = game.make_move('e1', 'e2')  # Red move
        print("e1-e2")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_10 = game.make_move('e10', 'e9')  # Black move
        print("e10-e9")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_11 = game.make_move('d3', 'c2')  # Red move (invalid)
        print("d3-c2 (invalid)")
        game.print_board()

        self.assertFalse(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_12 = game.make_move('f3', 'g2')  # Red move (invalid)
        print("f3-g2 (invalid)")
        game.print_board()

        self.assertFalse(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

        game.set_whose_turn("black")


        move_13 = game.make_move('d8', 'c9')  # Black move (invalid)
        print("d8-c9 (invalid)")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed
        # game.get_game_board().print_points_shadows()  # passed

        self.assertFalse(move_13)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_14 = game.make_move('f8', 'g9')  # Black move (invalid)
        print("f8-g9 (invalid)")
        game.print_board()

        game.get_game_board().print_pieces_shadows()  # passed
        game.get_game_board().print_points_shadows()  # passed

        self.assertFalse(move_14)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

    def test_20(self):   # passed
        """
        Test make_move for the red elephant. Should not be able to cross the
        river.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('c1', 'a3')  # Red move
        print("c1-a3")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.set_whose_turn("red")


        move_2 = game.make_move('a3', 'c5')  # Red move
        print("a3-c5")
        game.print_board()

        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.set_whose_turn("red")


        move_3 = game.make_move('c5', 'e7')  # Red move (invalid)
        print("c5-e7 (invalid)")
        game.print_board()

        game.get_game_board().print_pieces_shadows()  # passed

        self.assertFalse(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

    def test_21(self):   # passed
        """
        Test make_move for the red elephant. Should be blocked by an
        intervening piece on all corners.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('c1', 'e3')  # Red move
        print("c1-e3")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_2 = game.make_move('g1', 'i3')  # Red move
        print("g1-i3")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_3 = game.make_move('e7', 'e6')  # Black move
        print("e7-e6")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_4 = game.make_move('e6', 'e5')  # Black move
        print("e6-e5")
        game.print_board()

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_5 = game.make_move('e5', 'e4')  # Black move
        print("e5-e4")
        game.print_board()

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Block southeast diagonal
        move_6 = game.make_move('e4', 'f4')  # Black move
        print("e4-f4")
        game.print_board()

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_7 = game.make_move('f4', 'e4')  # Black move
        print("f4-e4")
        game.print_board()

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Block southwest diagonal
        move_8 = game.make_move('e4', 'd4')  # Black move
        print("e4-d4")
        game.print_board()

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_9 = game.make_move('d4', 'd3')  # Black move
        print("d4-d3")
        game.print_board()

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Block northwest diagonal
        move_10 = game.make_move('d3', 'd2')  # Black move
        print("d3-d2")
        game.print_board()

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_11 = game.make_move('d2', 'e2')  # Black move
        print("d2-e2")
        game.print_board()

        self.assertTrue(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertTrue(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_12 = game.make_move('e2', 'f2')  # Black move
        print("e2-f2")
        game.print_board()

        self.assertTrue(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed

    def test_22(self):   # passed
        """
        Test make_move for the black elephant. Should not be able to cross the
        river.
        """
        game = XiangqiGame()
        game.print_board()
        game.set_whose_turn("black")


        move_1 = game.make_move('g10', 'i8')  # Black move
        print("g10-i8")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        # Should not be able to cross the river
        move_2 = game.make_move('i8', 'g6')  # Black move
        print("i8-g6")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        game.get_game_board().print_pieces_shadows()  # passed

    def test_23(self):   # passed
        """
        Test make_move for the black elephant. Should be blocked by an
        intervening piece on all corners.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('e4', 'e5')  # Red move
        print("e4-e5")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_2 = game.make_move('e5', 'e6')  # Red move
        print("e5-e6")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_3 = game.make_move('e6', 'e7')  # Red move
        print("e6-e7")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_4 = game.make_move('g10', 'i8')  # Black move
        print("g10-i8")
        game.print_board()

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_5 = game.make_move('c10', 'e8')  # Black move
        print("c10-e8")
        game.print_board()

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

        # game.get_game_board().print_pieces_shadows()  # passed


        # Block the northwest diagonal
        move_6 = game.make_move('e7', 'd7')  # Red move
        print("e7-d7")
        game.print_board()

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_7 = game.make_move('d7', 'e7')  # Red move
        print("d7-e7")
        game.print_board()

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        # Block the northeast diagonal
        move_8 = game.make_move('e7', 'f7')  # Red move
        print("e7-f7")
        game.print_board()

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_9 = game.make_move('f7', 'f8')  # Red move
        print("f7-f8")
        game.print_board()

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")

        # game.get_game_board().print_pieces_shadows()  # passed


        # Block the southeast diagonal
        move_10 = game.make_move('f8', 'f9')  # Red move
        print("f8-f9")
        game.print_board()

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_11 = game.make_move('f9', 'e9')  # Red move
        print("f9-e9")
        game.print_board()

        self.assertTrue(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertTrue(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        # Block the southwest diagonal
        move_12 = game.make_move('e9', 'd9')  # Red move
        print("e9-d9")
        game.print_board()

        self.assertTrue(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")

        # game.get_game_board().print_pieces_shadows()  # passed

    def test_24(self):   # passed
        """
        Test make_move for the horse. Should be able to be blocked by a piece
        located one point horizontally or vertically adjacent to it.
        """
        game = XiangqiGame()
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        move_1 = game.make_move('e4', 'e5')  # Red move
        print("e4-e5")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('e7', 'e6')  # Black move
        print("e7-e6")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_3 = game.make_move('b1', 'c3')  # Red move
        print("b1-c3")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_4 = game.make_move('e6', 'e5')  # Black move
        print("e6-e5")
        game.print_board()

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_5 = game.make_move('c3', 'e4')  # Red move
        print("c3-e4")
        game.print_board()

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        # Check all movements of the horse if there are no blocking pieces
        move_6 = game.make_move('e5', 'd5')  # Black move
        print("e5-d5")
        game.print_board()

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        # Check horse movement if blocked at south orthogonal point
        move_7 = game.make_move('d5', 'e5')  # Black move
        print("d5-e5")
        game.print_board()

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_8 = game.make_move('e5', 'd5')  # Black move
        print("e5-d5")
        game.print_board()

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Check horse movement if blocked at west orthogonal point
        move_9 = game.make_move('d5', 'd4')  # Black move
        print("d5-d4")
        game.print_board()

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_10 = game.make_move('d4', 'd3')  # Black move
        print("d4-d3")
        game.print_board()

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Check horse movement if blocked at north orthogonal point
        move_11 = game.make_move('d3', 'e3')  # Black move
        print("d3-e3")
        game.print_board()

        self.assertTrue(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_12 = game.make_move('g7', 'g6')  # Black move
        print("g7-g6")
        game.print_board()

        self.assertTrue(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_13 = game.make_move('g6', 'g5')  # Black move
        print("g6-g5")
        game.print_board()

        self.assertTrue(move_13)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_14 = game.make_move('g5', 'f5')  # Black move
        print("g5-f5")
        game.print_board()

        self.assertTrue(move_14)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Check horse movement if blocked at north and east orthogonal
        # points
        move_15 = game.make_move('f5', 'f4')  # Black move
        print("f5-f4")
        game.print_board()

        self.assertTrue(move_15)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

        # game.get_game_board().print_pieces_shadows()  # passed


        move_16 = game.make_move('e3', 'e2')  # Black move
        print("e3-e2")
        game.print_board()

        self.assertTrue(move_16)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertTrue(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        # Check horse movement if blocked at east orthogonal point
        move_17 = game.make_move('d1', 'e2')  # Red move
        print("d1-e2")
        game.print_board()

        self.assertTrue(move_17)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.get_game_board().print_pieces_shadows()  # passed

    def test_25(self):   # passed
        """
        Test make_move for the chariot. Should be able to move and capture any
        distance orthogonally.
        """
        game = XiangqiGame()
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        game.set_whose_turn("black")

        move_1 = game.make_move('a10', 'a9')  # Black move
        print("a10-a9")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_2 = game.make_move('a7', 'a6')  # Black move
        print("a7-a6")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_3 = game.make_move('a6', 'a5')  # Black move
        print("a6-a5")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        # Check if black chariot shadows red soldier
        move_4 = game.make_move('a4', 'a5')  # Red move
        print("a4-a5")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        # Check if red chariot shadows black chariot
        # Also, check the east chariot movement after it has been implemented
        move_5 = game.make_move('a9', 'a5')  # Black move
        print("a9-a5")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_6 = game.make_move('a5', 'd5')  # Black move
        print("a5-d5")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Check chariot movement at right edge of board
        # Check west chariot movement
        move_7 = game.make_move('d5', 'i5')  # Black move
        print("d5-i5")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Check west chariot movement
        move_8 = game.make_move('i5', 'f5')  # Black move
        print("i5-f5")
        game.print_board()
        game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

    def test_26(self):   # passed
        """
        Test make_move for the cannon. Should be able to move any distance
        orthogonally without jumping, but should only be able to capture by
        jumping a single piece. Test north cannon movement.
        """
        game = XiangqiGame()
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        game.set_whose_turn("black")

        move_1 = game.make_move('b8', 'b5')  # Black move
        print("b8-b5")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_2 = game.make_move('b5', 'b1')  # Black move
        print("b5-b1")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")

    def test_27(self):   # passed
        """
        Test make_move for the cannon. Should be able to move any distance
        orthogonally without jumping, but should only be able to capture by
        jumping a single piece. Test south cannon movement.
        """
        game = XiangqiGame()
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        move_1 = game.make_move('b3', 'b6')  # Red move
        print("b3-b6")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_2 = game.make_move('b6', 'b7')  # Red move
        print("b6-b7")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_3 = game.make_move('b7', 'b10')  # Red move
        print("b7-b10")
        game.print_board()
        game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")

    def test_28(self):   # passed
        """
        Test make_move for the cannon. Should be able to move any distance
        orthogonally without jumping, but should only be able to capture by
        jumping a single piece. Test east cannon movement.
        """
        game = XiangqiGame()
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        move_1 = game.make_move('c4', 'c5')  # Red move
        print("c4-c5")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('c7', 'c6')  # Black move
        print("c7-c6")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_3 = game.make_move('c5', 'c6')  # Red move
        print("c5-c6")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_4 = game.make_move('b3', 'c3')  # Red move
        print("b3-c3")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_5 = game.make_move('c3', 'c10')  # Red move
        print("c3-c10")
        game.print_board()
        game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertTrue(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")

    def test_29(self):   # passed
        """
        Test make_move for the cannon. Should be able to move any distance
        orthogonally without jumping, but should only be able to capture by
        jumping a single piece. Test west cannon movement.
        """
        game = XiangqiGame()
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        move_1 = game.make_move('b3', 'b10')  # Red move
        print("b3-b10")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('i10', 'i9')  # Black move
        print("i10-i9")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_3 = game.make_move('b10', 'b9')  # Red move
        print("b10-b9")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_4 = game.make_move('d10', 'e9')  # Black move
        print("d10-e9")
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

    def test_30(self):   # passed
        """
        Test a sample game in which the black player wins.
        """
        game = XiangqiGame()
        game.print_board()
        # game.get_game_board().print_pieces_shadows()  # passed


        move_1 = game.make_move('c4', 'c5')  # Red move
        print("c4-c5")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('e7', 'e6')  # Black move
        print("e7-e6")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.get_game_board().print_pieces_shadows()  #



        move_3 = game.make_move('c5', 'b5')  # Red move (invalid)
        print("c5-b5")
        game.print_board()

        self.assertFalse(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_4 = game.make_move('c5', 'd5')  # Red move (invalid)
        print("c5-d5")
        game.print_board()

        self.assertFalse(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_5 = game.make_move('c5', 'c6')  # Red move
        print("c5-c6")
        game.print_board()

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_6 = game.make_move('e6', 'd6')  # Black move (invalid)
        print("e6-d6")
        game.print_board()

        self.assertFalse(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_7 = game.make_move('e6', 'f6')  # Black move (invalid)
        print("e6-f6")
        game.print_board()

        self.assertFalse(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_8 = game.make_move('e6', 'e5')  # Black move
        print("e6-e5")
        game.print_board()

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_9 = game.make_move('c6', 'd6')  # Red move
        print("c6-d6")
        game.print_board()

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_10 = game.make_move('e5', 'e4')  # Black move
        print("e5-e4")
        game.print_board()

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_11 = game.make_move('d6', 'd7')  # Red move
        print("d6-d7")
        game.print_board()

        self.assertTrue(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_12 = game.make_move('e4', 'f4')  # Black move (invalid)
        print("e4-f4")
        game.print_board()

        self.assertFalse(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_13 = game.make_move('f10', 'e9')  # Black move
        print("f10-e9")
        game.print_board()

        self.assertTrue(move_13)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_14 = game.make_move('b1', 'c3')  # Red move
        print("b1-c3")
        game.print_board()

        self.assertTrue(move_14)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_15 = game.make_move('h8', 'h1')  # Black move
        print("h8-h1")
        game.print_board()

        self.assertTrue(move_15)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_16 = game.make_move('c3', 'd5')  # Red move
        print("c3-d5")
        game.print_board()

        self.assertTrue(move_16)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_17 = game.make_move('h1', 'f1')  # Black move
        print("h1-f1")
        game.print_board()

        self.assertTrue(move_17)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_18 = game.make_move('d5', 'c7')  # Red move
        print("d5-c7")
        game.print_board()

        self.assertTrue(move_18)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_19 = game.make_move('f1', 'd1')  # Black move
        print("f1-d1")
        game.print_board()

        self.assertTrue(move_19)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_20 = game.make_move('d7', 'd8')  # Red move
        print("d7-d8")
        game.print_board()

        self.assertTrue(move_20)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        # Put red general in check
        move_21 = game.make_move('d1', 'a1')  # Black move
        print("d1-a1")
        game.print_board()

        self.assertTrue(move_21)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertTrue(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_22 = game.make_move('e1', 'f1')  # Red move (invalid)
        print("e1-f1")
        game.print_board()

        self.assertFalse(move_22)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertTrue(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_23 = game.make_move('e1', 'e2')  # Red move
        print("e1-e2")
        game.print_board()

        self.assertTrue(move_23)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_24 = game.make_move('i10', 'i8')  # Black move
        print("i10-i8")
        game.print_board()

        self.assertTrue(move_24)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_25 = game.make_move('d8', 'e8')  # Red move
        print("d8-e8")
        game.print_board()

        self.assertTrue(move_25)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_26 = game.make_move('i8', 'f8')  # Black move
        print("i8-f8")
        game.print_board()

        self.assertTrue(move_26)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        # Put black general in check
        move_27 = game.make_move('e8', 'e9')  # Red move
        print("e8-e9")
        game.print_board()

        self.assertTrue(move_27)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertTrue(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_28 = game.make_move('d10', 'e9')  # Black move
        print("d10-e9")
        game.print_board()

        self.assertTrue(move_28)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        # Set up to get red general in checkmate
        move_29 = game.make_move('i1', 'i2')  # Red move
        print("i1-i2")
        game.print_board()

        self.assertTrue(move_29)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_30 = game.make_move('a10', 'a9')  # Black move
        print("a10-a9")
        game.print_board()

        self.assertTrue(move_30)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_31 = game.make_move('i2', 'f2')  # Red move
        print("i2-f2")
        game.print_board()

        self.assertTrue(move_31)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_32 = game.make_move('a9', 'd9')  # Black move
        print("a9-d9")
        game.print_board()

        self.assertTrue(move_32)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_33 = game.make_move('f2', 'f1')  # Red move
        print("f2-f1")
        game.print_board()

        self.assertTrue(move_33)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_34 = game.make_move('d9', 'd3')  # Black move
        print("d9-d3")
        game.print_board()

        self.assertTrue(move_34)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_35 = game.make_move('f1', 'e1')  # Red move
        print("f1-e1")
        game.print_board()

        self.assertTrue(move_35)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_36 = game.make_move('f8', 'f3')  # Black move
        print("f8-f3")
        game.print_board()

        self.assertTrue(move_36)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_37 = game.make_move('c1', 'a3')  # Red move
        print("c1-a3")
        game.print_board()

        self.assertTrue(move_37)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_38 = game.make_move('a1', 'g1')  # Black move
        print("a1-g1")
        game.print_board()

        self.assertTrue(move_38)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_39 = game.make_move('b3', 'b5')  # Red move
        print("b3-b5")
        game.print_board()

        self.assertTrue(move_39)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_40 = game.make_move('g7', 'g6')  # Black move
        print("g7-g6")
        game.print_board()

        self.assertTrue(move_40)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_41 = game.make_move('h3', 'h5')  # Red move
        print("h3-h5")
        game.print_board()

        self.assertTrue(move_41)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        # Put red general in checkmate; black player wins
        move_42 = game.make_move('e4', 'e3')  # Black move
        print("e4-e3")
        game.print_board()

        self.assertTrue(move_42)
        self.assertEqual(game.get_game_state(), "BLACK_WON")
        self.assertTrue(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

    def test_31(self):   # passed
        """
        Test a sample game in which the red player wins.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('b3', 'b10')  # Red move
        print("b3-b10")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('e7', 'e6')  # Black move
        print("e7-e6")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_3 = game.make_move('e4', 'e5')  # Red move
        print("e4-e5")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_4 = game.make_move('g10', 'i8')  # Black move
        print("g10-i8")
        game.print_board()

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_5 = game.make_move('e5', 'e6')  # Red move
        print("e5-e6")
        game.print_board()

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_6 = game.make_move('a10', 'a8')  # Black move
        print("a10-a8")
        game.print_board()

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_7 = game.make_move('b10', 'd10')  # Red move
        print("b10-d10")
        game.print_board()

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_8 = game.make_move('i7', 'i6')  # Black move
        print("i7-i6")
        game.print_board()

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_9 = game.make_move('d10', 'f10')  # Red move
        print("d10-f10")
        game.print_board()

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_10 = game.make_move('i6', 'i5')  # Black move
        print("i6-i5")
        game.print_board()

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_11 = game.make_move('f10', 'i10')  # Red move
        print("f10-i10")
        game.print_board()

        self.assertTrue(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertTrue(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_12 = game.make_move('e10', 'e9')  # Black move
        print("e10-e9")
        game.print_board()

        self.assertTrue(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_13 = game.make_move('b1', 'c3')  # Red move
        print("b1-c3")
        game.print_board()

        self.assertTrue(move_13)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_14 = game.make_move('c10', 'e8')  # Black move
        print("c10-e8")
        game.print_board()

        self.assertTrue(move_14)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_15 = game.make_move('e6', 'e7')  # Red move
        print("e6-e7")
        game.print_board()

        self.assertTrue(move_15)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_16 = game.make_move('e8', 'g6')  # Black move
        print("e8-g6")
        game.print_board()

        self.assertTrue(move_16)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_17 = game.make_move('c3', 'e4')  # Red move
        print("c3-e4")
        game.print_board()

        self.assertTrue(move_17)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_18 = game.make_move('b8', 'b4')  # Black move
        print("b8-b4")
        game.print_board()

        self.assertTrue(move_18)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_19 = game.make_move('e4', 'd6')  # Red move
        print("e4-d6")
        game.print_board()

        self.assertTrue(move_19)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_20 = game.make_move('c7', 'c6')  # Black move
        print("c7-c6")
        game.print_board()

        self.assertTrue(move_20)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_21 = game.make_move('c4', 'c5')  # Red move
        print("c4-c5")
        game.print_board()

        self.assertTrue(move_21)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_22 = game.make_move('i5', 'i4')  # Black move
        print("i5-i4")
        game.print_board()

        self.assertTrue(move_22)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_23 = game.make_move('c5', 'c6')  # Red move
        print("c5-c6")
        game.print_board()

        self.assertTrue(move_23)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_24 = game.make_move('i4', 'i3')  # Black move
        print("i4-i3")
        game.print_board()

        self.assertTrue(move_24)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_25 = game.make_move('c6', 'c7')  # Red move
        print("c6-c7")
        game.print_board()

        self.assertTrue(move_25)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.set_whose_turn("red")


        move_26 = game.make_move('c7', 'd7')  # Red move
        print("c7-d7")
        game.print_board()

        self.assertTrue(move_26)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.set_whose_turn("red")


        move_27 = game.make_move('d7', 'd8')  # Red move
        print("d7-d8")
        game.print_board()

        self.assertTrue(move_27)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.set_whose_turn("red")


        move_28 = game.make_move('e7', 'e8')  # Red move
        print("e7-e8")
        game.print_board()

        self.assertTrue(move_28)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertTrue(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_29 = game.make_move('e9', 'f9')  # Black move
        print("e9-f9")
        game.print_board()

        self.assertTrue(move_29)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_30 = game.make_move('d8', 'd9')  # Red move
        print("d8-d9")
        game.print_board()

        self.assertTrue(move_30)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_31 = game.make_move('h8', 'h6')  # Black move
        print("h8-h6")
        game.print_board()

        self.assertTrue(move_31)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_32 = game.make_move('d9', 'e9')  # Red move
        print("d9-e9")
        game.print_board()

        self.assertTrue(move_32)
        self.assertEqual(game.get_game_state(), "RED_WON")
        self.assertFalse(game.is_in_check("red"))
        self.assertTrue(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

    def test_32(self):   #
        """
        Test a sample game in which the black player is stalemated.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('b3', 'b10')  # Red move
        print("b3-b10")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('e7', 'e6')  # Black move
        print("e7-e6")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_3 = game.make_move('e4', 'e5')  # Red move
        print("e4-e5")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_4 = game.make_move('g10', 'i8')  # Black move
        print("g10-i8")
        game.print_board()

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_5 = game.make_move('e5', 'e6')  # Red move
        print("e5-e6")
        game.print_board()

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_6 = game.make_move('a10', 'a8')  # Black move
        print("a10-a8")
        game.print_board()

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_7 = game.make_move('b10', 'd10')  # Red move
        print("b10-d10")
        game.print_board()

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_8 = game.make_move('i7', 'i6')  # Black move
        print("i7-i6")
        game.print_board()

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_9 = game.make_move('d10', 'f10')  # Red move
        print("d10-f10")
        game.print_board()

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_10 = game.make_move('i6', 'i5')  # Black move
        print("i6-i5")
        game.print_board()

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_11 = game.make_move('f10', 'i10')  # Red move
        print("f10-i10")
        game.print_board()

        self.assertTrue(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertTrue(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_12 = game.make_move('e10', 'e9')  # Black move
        print("e10-e9")
        game.print_board()

        self.assertTrue(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_13 = game.make_move('b1', 'c3')  # Red move
        print("b1-c3")
        game.print_board()

        self.assertTrue(move_13)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_14 = game.make_move('c10', 'e8')  # Black move
        print("c10-e8")
        game.print_board()

        self.assertTrue(move_14)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_15 = game.make_move('e6', 'e7')  # Red move
        print("e6-e7")
        game.print_board()

        self.assertTrue(move_15)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_16 = game.make_move('e8', 'g6')  # Black move
        print("e8-g6")
        game.print_board()

        self.assertTrue(move_16)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_17 = game.make_move('c3', 'e4')  # Red move
        print("c3-e4")
        game.print_board()

        self.assertTrue(move_17)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_18 = game.make_move('b8', 'b4')  # Black move
        print("b8-b4")
        game.print_board()

        self.assertTrue(move_18)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_19 = game.make_move('e4', 'd6')  # Red move
        print("e4-d6")
        game.print_board()

        self.assertTrue(move_19)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_20 = game.make_move('c7', 'c6')  # Black move
        print("c7-c6")
        game.print_board()

        self.assertTrue(move_20)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_21 = game.make_move('c4', 'c5')  # Red move
        print("c4-c5")
        game.print_board()

        self.assertTrue(move_21)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_22 = game.make_move('i5', 'i4')  # Black move
        print("i5-i4")
        game.print_board()

        self.assertTrue(move_22)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_23 = game.make_move('c5', 'c6')  # Red move
        print("c5-c6")
        game.print_board()

        self.assertTrue(move_23)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_24 = game.make_move('i4', 'i3')  # Black move
        print("i4-i3")
        game.print_board()

        self.assertTrue(move_24)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_25 = game.make_move('c6', 'c7')  # Red move
        print("c6-c7")
        game.print_board()

        self.assertTrue(move_25)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.set_whose_turn("red")


        move_26 = game.make_move('c7', 'd7')  # Red move
        print("c7-d7")
        game.print_board()

        self.assertTrue(move_26)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.set_whose_turn("red")


        move_27 = game.make_move('d7', 'd8')  # Red move
        print("d7-d8")
        game.print_board()

        self.assertTrue(move_27)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        game.set_whose_turn("red")


        move_28 = game.make_move('e7', 'e8')  # Red move
        print("e7-e8")
        game.print_board()

        self.assertTrue(move_28)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertTrue(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_29 = game.make_move('e9', 'f9')  # Black move
        print("e9-f9")
        game.print_board()

        self.assertTrue(move_29)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_30 = game.make_move('d8', 'd9')  # Red move
        print("d8-d9")
        game.print_board()

        self.assertTrue(move_30)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_31 = game.make_move('a4', 'a5')  # Red move
        print("a4-a5")
        game.print_board()

        self.assertTrue(move_31)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_32 = game.make_move('a1', 'a4')  # Red move
        print("a1-a4")
        game.print_board()

        self.assertTrue(move_32)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_33 = game.make_move('a4', 'b4')  # Red move
        print("a4-b4")
        game.print_board()

        self.assertTrue(move_33)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_34 = game.make_move('a5', 'a6')  # Red move
        print("a5-a6")
        game.print_board()

        self.assertTrue(move_34)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_35 = game.make_move('a6', 'a7')  # Red move
        print("a6-a7")
        game.print_board()

        self.assertTrue(move_35)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_36 = game.make_move('a7', 'a8')  # Red move
        print("a7-a8")
        game.print_board()

        self.assertTrue(move_36)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_37 = game.make_move('b4', 'b5')  # Red move
        print("b4-b5")
        game.print_board()

        self.assertTrue(move_37)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_38 = game.make_move('b5', 'g5')  # Red move
        print("b5-g5")
        game.print_board()

        self.assertTrue(move_38)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_39 = game.make_move('g5', 'g6')  # Red move
        print("g5-g6")
        game.print_board()

        self.assertTrue(move_39)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_40 = game.make_move('g6', 'g7')  # Red move
        print("g6-g7")
        game.print_board()

        self.assertTrue(move_40)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_41 = game.make_move('g7', 'i7')  # Red move
        print("g7-i7")
        game.print_board()

        self.assertTrue(move_41)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_42 = game.make_move('i7', 'i8')  # Red move
        print("i7-i8")
        game.print_board()

        self.assertTrue(move_42)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_43 = game.make_move('i8', 'i3')  # Red move
        print("i8-i3")
        game.print_board()

        self.assertTrue(move_43)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_44 = game.make_move('h3', 'h10')  # Red move
        print("h3-h10")
        game.print_board()

        self.assertTrue(move_44)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_45 = game.make_move('h8', 'h2')  # Black move
        print("h8-h2")
        game.print_board()

        self.assertTrue(move_45)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_46 = game.make_move('i3', 'g3')  # Red move
        print("i3-g3")
        game.print_board()

        self.assertTrue(move_46)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_47 = game.make_move('g3', 'g2')  # Red move
        print("g3-g2")
        game.print_board()

        self.assertTrue(move_47)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_48 = game.make_move('i1', 'i2')  # Red move
        print("i1-i2")
        game.print_board()

        self.assertTrue(move_48)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_49 = game.make_move('h10', 'h3')  # Red move
        print("h10-h3")
        game.print_board()

        self.assertTrue(move_49)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_50 = game.make_move('a8', 'a9')  # Red move
        print("a8-a9")
        game.print_board()

        self.assertTrue(move_50)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_51 = game.make_move('a9', 'a10')  # Red move
        print("a9-a10")
        game.print_board()

        self.assertTrue(move_51)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_52 = game.make_move('a10', 'b10')  # Red move
        print("a10-b10")
        game.print_board()

        self.assertTrue(move_52)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_53 = game.make_move('b10', 'c10')  # Red move
        print("b10-c10")
        game.print_board()

        self.assertTrue(move_53)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        move_54 = game.make_move('c10', 'd10')  # Red move
        print("c10-d10")
        game.print_board()

        self.assertTrue(move_54)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")
        game.set_whose_turn("red")


        # Put black player in stalemate - red player wins
        move_55 = game.make_move('d10', 'e10')  # Red move
        print("d10-e10")
        game.print_board()

        self.assertTrue(move_55)
        self.assertEqual(game.get_game_state(), "RED_WON")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

    def test_33(self):   # passed
        """
        Test a sample game in which the red player is stalemated.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('a4', 'a5')  # Red move
        print("a4-a5")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_2 = game.make_move('a7', 'a6')  # Black move
        print("a7-a6")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_3 = game.make_move('a6', 'a5')  # Black move
        print("a6-a5")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_4 = game.make_move('a5', 'b5')  # Black move
        print("a5-b5")
        game.print_board()

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_5 = game.make_move('a10', 'a1')  # Black move
        print("a10-a1")
        game.print_board()

        self.assertTrue(move_5)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_6 = game.make_move('a1', 'b1')  # Black move
        print("a1-b1")
        game.print_board()

        self.assertTrue(move_6)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_7 = game.make_move('b1', 'c1')  # Black move
        print("b1-c1")
        game.print_board()

        self.assertTrue(move_7)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_8 = game.make_move('c1', 'c2')  # Black move
        print("c1-c2")
        game.print_board()

        self.assertTrue(move_8)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_9 = game.make_move('c2', 'i2')  # Black move
        print("c2-i2")
        game.print_board()

        self.assertTrue(move_9)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_10 = game.make_move('i2', 'i1')  # Black move
        print("i2-i1")
        game.print_board()

        self.assertTrue(move_10)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_11 = game.make_move('i1', 'h1')  # Black move
        print("i1-h1")
        game.print_board()

        self.assertTrue(move_11)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_12 = game.make_move('h1', 'g1')  # Black move
        print("h1-g1")
        game.print_board()

        self.assertTrue(move_12)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_13 = game.make_move('g1', 'f1')  # Black move
        print("g1-f1")
        game.print_board()

        self.assertTrue(move_13)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertTrue(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_14 = game.make_move('f1', 'f3')  # Black move
        print("f1-f3")
        game.print_board()

        self.assertTrue(move_14)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_15 = game.make_move('f3', 'h3')  # Black move
        print("f3-h3")
        game.print_board()

        self.assertTrue(move_15)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_16 = game.make_move('h3', 'b3')  # Black move
        print("h3-b3")
        game.print_board()

        self.assertTrue(move_16)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_17 = game.make_move('b3', 'b4')  # Black move
        print("b3-b4")
        game.print_board()

        self.assertTrue(move_17)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_18 = game.make_move('b4', 'c4')  # Black move
        print("b4-c4")
        game.print_board()

        self.assertTrue(move_18)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_19 = game.make_move('c4', 'e4')  # Black move
        print("c4-e4")
        game.print_board()

        self.assertTrue(move_19)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertTrue(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_20 = game.make_move('e4', 'g4')  # Black move
        print("e4-g4")
        game.print_board()

        self.assertTrue(move_20)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_21 = game.make_move('g4', 'i4')  # Black move
        print("g4-i4")
        game.print_board()

        self.assertTrue(move_21)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_22 = game.make_move('i4', 'f4')  # Black move
        print("i4-f4")
        game.print_board()

        self.assertTrue(move_22)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_23 = game.make_move('i10', 'i9')  # Black move
        print("i10-i9")
        game.print_board()

        self.assertTrue(move_23)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_24 = game.make_move('i9', 'd9')  # Black move
        print("i9-d9")
        game.print_board()

        self.assertTrue(move_24)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_25 = game.make_move('d9', 'd4')  # Black move
        print("d9-d4")
        game.print_board()

        self.assertTrue(move_25)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")


        move_26 = game.make_move('d1', 'e2')  # Red move
        print("d1-e2")
        game.print_board()

        self.assertTrue(move_26)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")


        move_27 = game.make_move('e7', 'e6')  # Black move
        print("e7-e6")
        game.print_board()

        self.assertTrue(move_27)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        move_28 = game.make_move('e6', 'e5')  # Black move
        print("e6-e5")
        game.print_board()

        self.assertTrue(move_28)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
        game.set_whose_turn("black")


        # Put red player in stalemate
        move_29 = game.make_move('e5', 'f5')  # Black move
        print("e5-f5")
        game.print_board()

        self.assertTrue(move_29)
        self.assertEqual(game.get_game_state(), "BLACK_WON")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

    def test_34(self):
        """
        Test a very simple game.
        """
        game = XiangqiGame()

        move_result = game.make_move('c1', 'e3')
        black_in_check = game.is_in_check('black')
        game.make_move('e7', 'e6')
        state = game.get_game_state()

        game.print_board()
        self.assertEqual(move_result, True)
        self.assertEqual(black_in_check, False)
        self.assertEqual(state, "UNFINISHED")

    def test_35(self):   # passed
        """
        Test whether a cannon is able to move north for its first move.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('b3', 'b2')  # Red move
        print("b3-b2")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        move_2 = game.make_move('b8', 'b3')  # Black move
        print("b8-b3")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

        move_3 = game.make_move('h3', 'h2')  # Red move
        print("h3-h2")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        move_4 = game.make_move('h8', 'h5')  # Black move
        print("h8-h5")
        game.print_board()

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

    def test_36(self):   # passed
        """
        Test whether a cannon is able to move east for its first move.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('b3', 'g3')  # Red move
        print("b3-g3")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        move_2 = game.make_move('b8', 'g8')  # Black move
        print("b8-g8")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

        move_3 = game.make_move('h3', 'i3')  # Red move
        print("h3-i3")
        game.print_board()

        self.assertTrue(move_3)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        move_4 = game.make_move('h8', 'i8')  # Black move
        print("h8-i8")
        game.print_board()

        self.assertTrue(move_4)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

    def test_37(self):   # passed
        """
        Test whether a cannon is able to move south for its first move.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('b3', 'b7')  # Red move
        print("b3-b7")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        move_2 = game.make_move('b8', 'b9')  # Black move
        print("b8-b9")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")

    def test_38(self):   # passed
        """
        Test whether a cannon is able to move west for its first move.
        """
        game = XiangqiGame()
        game.print_board()

        move_1 = game.make_move('h3', 'c3')  # Red move
        print("h3-c3")
        game.print_board()

        self.assertTrue(move_1)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "black")

        move_2 = game.make_move('h8', 'c8')  # Black move
        print("h8-c8")
        game.print_board()

        self.assertTrue(move_2)
        self.assertEqual(game.get_game_state(), "UNFINISHED")
        self.assertFalse(game.is_in_check("red"))
        self.assertFalse(game.is_in_check("black"))
        self.assertEqual(game.get_whose_turn(), "red")
