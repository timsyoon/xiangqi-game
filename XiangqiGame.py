# Author: Timothy Yoon
# Date of Original Submission: March 10, 2020
# Description: This file defines a class named XiangqiGame for playing an
# abstract board game called xiangqi. In this strategy game, two players (red
# and black) move pieces on a board with the objective of checkmating the
# opponent's "general" piece. The class is implemented based on the "Board",
# "Rules", and "Pieces" sections of the following Wikipedia page:
# https://en.wikipedia.org/wiki/Xiangqi. Other classes include Board, Point,
# Piece, General, Advisor, Elephant, Horse, Chariot, Cannon, and Soldier. All
# class data members are private.
#
# Rules regarding perpetual check or chasing are not implemented, but the
# class is designed to correctly handle a stalemate, as well as all piece-
# specific rules (e.g. elephants can't cross the river). Locations on the
# board are initially specified using algebraic notation, with columns labeled
# a-i (where the letter is typically converted to an integer from 1-9) and rows
# labeled 1-10, with row 1 being the red side and row 10 the black side. Both
# column and row numbers are 1-based.
#
# Language note: Throughout this file, the term "shadow" and its variants are
# frequently used. If a player's piece "shadows" a point, this means that the
# piece can legally move into the point in the player's next turn. Legal moves
# include those where a player's own general is put or left in check, since the
# current implementation reverses such moves.


class XiangqiGame:
    """
    Represent the playing of a board game called xiangqi. An object of the
    class has a board (via composition), and the other data members have
    getter and setter methods. In particular, information on the game state,
    on whether either player is in check, and on whose turn it is can be
    retrieved and updated. A class object can also try to make a move between
    two points on the board. The print_board method displays a colored board
    on the console, and quantify_location converts a letter-number formatted
    string into a number-number formatted tuple.
    """
    def __init__(self):
        """
        Create a XiangqiGame object. The data members are initialized and
        include a board, the game state, whether either of the players is in
        check, and whose turn it is.
        """
        self._board = Board()
        self._game_state = "UNFINISHED"
        self._red_in_check = False
        self._black_in_check = False
        self._whose_turn = "red"        # Red player starts the game

    def get_game_board(self):
        """
        Return the board data member.
        """
        return self._board

    def get_game_state(self):
        """
        Return the current game state, which can be "UNFINISHED", "RED_WON",
        or "BLACK_WON". The game state is largely determined by the make_move
        method, which among other things, checks for cases of checkmate and
        stalemate.
        """
        return self._game_state

    def set_game_state(self, new_state):
        """
        Update the current game state to "UNFINISHED" (not possible in
        practice), "RED_WON", or "BLACK_WON".
        """
        self._game_state = new_state

    def remove_from_check(self, player_color):
        """
        Take as a parameter either "red" or "black" for the player color and
        indicate that the player's general is no longer in check.
        """
        if player_color == "red":
            self._red_in_check = False

        if player_color == "black":
            self._black_in_check = False

    def get_whose_turn(self):
        """
        Return which player's turn it is currently.
        """
        return self._whose_turn

    def set_whose_turn(self, player_color):
        """
        Take as a parameter either "red" or "black" for the player color and
        update which player's turn it is currently.
        """
        self._whose_turn = player_color

    def make_move(self, move_from, move_to):
        """
        Take as parameters two strings that represent the point moved from and
        the point moved to. If the point being moved from is empty or does not
        contain a piece belonging to the player whose turn it is, or if the
        point moved to has a piece owned by the player whose turn it is, or if
        the game has already been won, or if the indicated move is not legal,
        return False. Otherwise, among other actions, make the indicated move,
        remove any captured piece, update the game state if necessary,
        update whose turn it is, and return True.
        """
        # Convert the letter-number strings to number-number tuples
        source_coord = self.quantify_location(move_from)
        dest_coord = self.quantify_location(move_to)
        brd = self._board.get_board()
        is_own_general_in_check = False

        # Check the source coordinate

        # If the point being moved from is empty, return False
        if brd[source_coord].get_contains() is None:
            return False

        # If the point being moved from does not contain a piece belonging
        # to the player whose turn it is, return False
        if (brd[source_coord].get_contains().get_color()
                != self.get_whose_turn()):
            return False

        # Check the destination coordinate

        # If the point moved to has a piece owned by the player whose turn it
        # is, return False
        if brd[dest_coord].get_contains() is not None:
            if (brd[dest_coord].get_contains().get_color()
                    == self.get_whose_turn()):
                return False

        curr_piece = brd[source_coord].get_contains()

        # If the move is not legal (i.e. if the destination coordinate is not
        # in the piece's list of points shadowed), return False
        if dest_coord not in curr_piece.get_shadows():
            return False

        # If the game has already been won, return False
        if self.get_game_state() != "UNFINISHED":   # If either player has won
            return False

        # If the move is legal, make the indicated move
        if dest_coord in curr_piece.get_shadows():

            # Remove any captured piece, but temporarily hold it in case the
            # move needs to be reversed
            discarded_piece = brd[dest_coord].get_contains()

            # Have the destination point hold the piece being moved
            brd[dest_coord].set_contains(curr_piece)
            curr_piece.set_col(dest_coord[0])   # Update the piece's column
            curr_piece.set_row(dest_coord[1])   # Update the piece's row

            # Remove the source point's contents
            brd[source_coord].set_contains(None)

            # Update _shadows for every piece on the board
            for coord in brd:
                if brd[coord].get_contains() is not None:
                    piece = brd[coord].get_contains()
                    piece.update_shadows(brd)

            # Update _shadowed_by for every point on the board
            self._board.update_points_shadows()

            # Look for the player's own general
            for coord in brd:
                if brd[coord].get_contains() is not None:
                    piece = brd[coord].get_contains()
                    if piece.get_color() == self.get_whose_turn():

                        # If the general is found
                        if piece.get_type_id() == 'G':
                            gen_col = piece.get_col()
                            gen_row = piece.get_row()
                            if (len(brd[(gen_col, gen_row)].get_shadowed_by())
                                    >= 1):
                                is_own_general_in_check = True

            # If the player's own general is in check, reverse the move
            if is_own_general_in_check:
                # Have the moved piece go back to its former point
                brd[source_coord].set_contains(curr_piece)
                curr_piece.set_col(source_coord[0])  # Restore the piece's col
                curr_piece.set_row(source_coord[1])  # Restore the piece's row

                # Have the discarded piece go back to its former point
                brd[dest_coord].set_contains(discarded_piece)

                # Restore _shadows for every piece on the board
                for coord in brd:
                    if brd[coord].get_contains() is not None:
                        piece = brd[coord].get_contains()
                        piece.update_shadows(brd)

                # Restore _shadowed_by for every point on the board
                self._board.update_points_shadows()

                return False

        # Update the game state if necessary

        # If either player's general is shadowed, put it in check

        # Check whether the red general is in check
        if self.is_in_check("red"):
            self._red_in_check = True
        else:
            self._red_in_check = False

        # Check whether the black general is in check
        if self.is_in_check("black"):
            self._black_in_check = True
        else:
            self._black_in_check = False

        # If the red general is in check, and it cannot escape being in
        # check, then it is checkmated and the black player wins:
        if self._red_in_check:
            if self.is_in_checkmate("red"):
                self._game_state = "BLACK_WON"

        # If the black general is in check, and it cannot escape being in
        # check, then it is checkmated and the red player wins:
        if self._black_in_check:
            if self.is_in_checkmate("black"):
                self._game_state = "RED_WON"

        # Check whether the opponent is stalemated (i.e. is not in check but
        # has no legal moves)

        if self._whose_turn == "red":
            # If the black player is stalemated, the red player wins
            if self.is_in_stalemate("black"):
                self._game_state = "RED_WON"

        if self._whose_turn == "black":
            # If the red player is stalemated, the black player wins
            if self.is_in_stalemate("red"):
                self._game_state = "BLACK_WON"

        # Update whose turn it is
        if self._whose_turn == "red":
            self._whose_turn = "black"
        else:
            self._whose_turn = "red"

        return True

    def is_in_check(self, player_color):
        """
        Take as a parameter either "red" or "black" for the player color and
        return True if that player's general is in check, but False otherwise.
        """
        brd = self._board.get_board()

        # Check whether the red general is in check
        if player_color == "red":
            for coord in brd:

                # If the point has a piece
                if brd[coord].get_contains() is not None:
                    piece = brd[coord].get_contains()

                    # If the piece is red
                    if piece.get_color() == "red":

                        # If the piece is a general
                        if piece.get_type_id() == 'G':
                            gen_col = piece.get_col()
                            gen_row = piece.get_row()

                            # If there is at least one piece shadowing the
                            # red general's point
                            if (len(brd[(gen_col, gen_row)].get_shadowed_by())
                                    >= 1):
                                return True

                            # If there are no pieces shadowing the red
                            # general's point
                            else:
                                return False

        # Check whether the black general is in check
        if player_color == "black":
            for coord in brd:

                # If the point has a piece
                if brd[coord].get_contains() is not None:
                    piece = brd[coord].get_contains()

                    # If the piece is black
                    if piece.get_color() == "black":

                        # If the piece is a general
                        if piece.get_type_id() == 'G':
                            gen_col = piece.get_col()
                            gen_row = piece.get_row()

                            # If there is at least one piece shadowing the
                            # black general's point
                            if (len(brd[(gen_col, gen_row)].get_shadowed_by())
                                    >= 1):
                                return True

                            # If there are no pieces shadowing the black
                            # general's point
                            else:
                                return False

    def is_in_checkmate(self, player_color):
        """
        Take as a parameter a player color and return True if that player's
        general has been checkmated, and False otherwise.
        """
        board = self._board.get_board()

        # Assume that the general cannot escape check, unless proven otherwise
        can_escape_check = False

        # For every piece on the board that has the player color, attempt all
        # moves for that piece, checking to see if any move puts the general
        # out of check
        for coord in board:

            # If the point has a piece
            if board[coord].get_contains() is not None:
                test_piece = board[coord].get_contains()

                # If the test piece matches the player_color
                if test_piece.get_color() == player_color:
                    old_col = test_piece.get_col()
                    old_row = test_piece.get_row()

                    shadows = test_piece.get_shadows()

                    # Attempt moving the test piece into all of its shadows
                    for shadow in shadows:

                        # If the point is empty
                        if board[shadow].get_contains() is None:

                            # Move the test piece into the point
                            board[shadow].set_contains(test_piece)
                            test_piece.set_col(shadow[0])  # Update column
                            test_piece.set_row(shadow[1])  # Update row

                            # Remove the test piece from its former point
                            board[(old_col, old_row)].set_contains(None)

                            # Update _shadows for every piece on the board
                            for coordt in board:
                                if board[coordt].get_contains() is not None:
                                    piece = board[coordt].get_contains()
                                    piece.update_shadows(board)

                            # Update _shadowed_by for every point on the board
                            self._board.update_points_shadows()

                            if not self.is_in_check(player_color):
                                can_escape_check = True

                            # Restore test_piece to its original position
                            board[(old_col, old_row)].set_contains(test_piece)
                            test_piece.set_col(old_col)  # Restore column
                            test_piece.set_row(old_row)  # Restore row

                            # Remove the test_piece from its shadow
                            board[shadow].set_contains(None)

                            # Restore _shadows for every piece on the board
                            for coordin in board:
                                if board[coordin].get_contains() is not None:
                                    piece = board[coordin].get_contains()
                                    piece.update_shadows(board)

                            # Restore _shadowed_by for every point on the board
                            self._board.update_points_shadows()

                        # If the point has a piece
                        else:
                            target_piece = board[shadow].get_contains()

                            # If the piece belongs to the opponent
                            if target_piece.get_color() != player_color:

                                # Move the test piece into the point occupied
                                # by the target piece
                                board[shadow].set_contains(test_piece)
                                test_piece.set_col(shadow[0])  # Update column
                                test_piece.set_row(shadow[1])  # Update row

                                # Remove the test piece from its former point
                                board[(old_col, old_row)].set_contains(None)

                                # Update _shadows for every piece on the board
                                for coordt in board:
                                    point = board[coordt]
                                    if point.get_contains() is not None:
                                        piece = point.get_contains()
                                        piece.update_shadows(board)

                                # Update _shadowed_by for every point on the
                                # board
                                self._board.update_points_shadows()

                                if not self.is_in_check(player_color):
                                    can_escape_check = True

                                # Restore test_piece to its original position
                                board[(old_col, old_row)].set_contains(
                                    test_piece)
                                test_piece.set_col(old_col)  # Restore column
                                test_piece.set_row(old_row)  # Restore row

                                # Restore target_piece to its original position
                                board[shadow].set_contains(target_piece)

                                # Restore _shadows for every piece on the board
                                for coordnt in board:
                                    point = board[coordnt]
                                    if point.get_contains() is not None:
                                        piece = board[coordnt].get_contains()
                                        piece.update_shadows(board)

                                # Restore _shadowed_by for every point on the
                                # board
                                self._board.update_points_shadows()

        if can_escape_check:
            return False
        else:
            return True

    def is_in_stalemate(self, player_color):
        """
        Take as a parameter a player color and return True if that player has
        been stalemated (i.e. is not in check but has no legal moves), and
        False otherwise.
        """
        board = self._board.get_board()

        # Assume that the player has been stalemated, unless proven otherwise
        has_legal_move = False

        # For every piece on the board that has the player color, attempt all
        # moves for that piece, checking to see if any move is valid and
        # does not put the general in check
        for coord in board:

            # If the point has a piece
            if board[coord].get_contains() is not None:
                test_piece = board[coord].get_contains()

                # If the test piece matches the player_color
                if test_piece.get_color() == player_color:
                    old_col = test_piece.get_col()
                    old_row = test_piece.get_row()

                    shadows = test_piece.get_shadows()

                    # Attempt moving the test piece into all of its shadows
                    for shadow in shadows:

                        # If the point is empty
                        if board[shadow].get_contains() is None:

                            # Move the test piece into the point
                            board[shadow].set_contains(test_piece)
                            test_piece.set_col(shadow[0])  # Update column
                            test_piece.set_row(shadow[1])  # Update row

                            # Remove the test piece from its former point
                            board[(old_col, old_row)].set_contains(None)

                            # Update _shadows for every piece on the board
                            for coordt in board:
                                if board[coordt].get_contains() is not None:
                                    piece = board[coordt].get_contains()
                                    piece.update_shadows(board)

                            # Update _shadowed_by for every point on the board
                            self._board.update_points_shadows()

                            if not self.is_in_check(player_color):
                                has_legal_move = True

                            # Restore test_piece to its original position
                            board[(old_col, old_row)].set_contains(test_piece)
                            test_piece.set_col(old_col)  # Restore column
                            test_piece.set_row(old_row)  # Restore row

                            # Remove the test_piece from its shadow
                            board[shadow].set_contains(None)

                            # Restore _shadows for every piece on the board
                            for coordin in board:
                                if board[coordin].get_contains() is not None:
                                    piece = board[coordin].get_contains()
                                    piece.update_shadows(board)

                            # Restore _shadowed_by for every point on the board
                            self._board.update_points_shadows()

                        # If the point has a piece
                        else:
                            target_piece = board[shadow].get_contains()

                            # If the piece belongs to the opponent
                            if target_piece.get_color() != player_color:

                                # Move the test piece into the point occupied
                                # by the target piece
                                board[shadow].set_contains(test_piece)
                                test_piece.set_col(shadow[0])  # Update column
                                test_piece.set_row(shadow[1])  # Update row

                                # Remove the test piece from its former point
                                board[(old_col, old_row)].set_contains(None)

                                # Update _shadows for every piece on the board
                                for coordt in board:
                                    point = board[coordt]
                                    if point.get_contains() is not None:
                                        piece = point.get_contains()
                                        piece.update_shadows(board)

                                # Update _shadowed_by for every point on the
                                # board
                                self._board.update_points_shadows()

                                if not self.is_in_check(player_color):
                                    has_legal_move = True

                                # Restore test_piece to its original position
                                board[(old_col, old_row)].set_contains(
                                    test_piece)
                                test_piece.set_col(old_col)  # Restore column
                                test_piece.set_row(old_row)  # Restore row

                                # Restore target_piece to its original position
                                board[shadow].set_contains(target_piece)

                                # Restore _shadows for every piece on the board
                                for coordnt in board:
                                    point = board[coordnt]
                                    if point.get_contains() is not None:
                                        piece = board[coordnt].get_contains()
                                        piece.update_shadows(board)

                                # Restore _shadowed_by for every point on the
                                # board
                                self._board.update_points_shadows()

        # If the player has a legal move, then it is not in stalemate
        if has_legal_move:
            return False
        else:
            return True

    def print_board(self):
        """
        Print the board of the game for testing and debugging purposes. Code
        and ideas from https://ozzmaker.com/add-colour-to-text-in-python/ are
        used. However, the foreground and background codes listed on the
        website did not seem to match the colors actually displayed, perhaps
        because the Python file was run on a Windows-based system.
        """
        board = self._board.get_board()

        # Print the first header row
        print("\033[0;30;47m    a", end = "  ")
        print("\033[0;30;47mb", end = "  ")
        print("\033[0;30;47mc", end = "  ")
        print("\033[0;90;47md", end = "  ")
        print("\033[0;90;47me", end = "  ")
        print("\033[0;90;47mf", end = "  ")
        print("\033[0;30;47mg", end = "  ")
        print("\033[0;30;47mh", end = "  ")
        print("\033[0;30;47mi", end = "    ")
        print("\033[0;97;30m")

        # Print the second header row
        print("\033[0;30;47m    1", end = "  ")
        print("\033[0;30;47m2", end = "  ")
        print("\033[0;30;47m3", end = "  ")
        print("\033[0;90;47m4", end = "  ")
        print("\033[0;90;47m5", end = "  ")
        print("\033[0;90;47m6", end = "  ")
        print("\033[0;30;47m7", end = "  ")
        print("\033[0;30;47m8", end = "  ")
        print("\033[0;30;47m9", end = "    ")
        print("\033[0;97;30m")

        # Print row 1 of the game board
        print("\033[0;30;47m 1", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 1)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 1)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 1)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 1)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 1)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 1", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print row 2 of the game board
        print("\033[0;30;47m 2", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 2)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 2)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 2)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 2)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 2)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 2", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print row 3 of the game board
        print("\033[0;30;47m 3", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 3)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 3)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 3)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 3)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 3)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 3", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print row 4 of the game board
        print("\033[0;30;47m 4", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 4)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 4)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 4)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 4)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 4)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 4", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print row 5 of the game board
        print("\033[0;30;47m 5", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 5)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 5)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 5)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 5)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 5)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 5", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print river
        print("\033[0;30;44m", end="                                 ")
        print("\033[0;29;48m", end="\n")

        # Print row 6 of the game board
        print("\033[0;30;47m 6", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 6)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 6)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 6)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 6)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 6)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 6", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print row 7 of the game board
        print("\033[0;30;47m 7", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 7)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 7)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 7)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 7)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 7)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 7", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print row 8 of the game board
        print("\033[0;30;47m 8", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 8)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 8)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 8)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 8)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 8)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 8", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print row 9 of the game board
        print("\033[0;30;47m 9", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 9)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 9)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 9)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 9)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 9)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 9", end=" ")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print row 10 of the game board
        print("\033[0;30;47m10", end=" ")   # Row label at beginning

        # Print columns a-i (1-9)
        for num in range(1, 10):

            # Print left bracket
            print("\033[0;29;48m[", end = "")

            # If the point on the board does not have a piece, print a blank
            # space and right bracket
            if board[(num, 10)].get_contains() is None:
                print("\033[0;29;48m ]", end="")

            # If the point on the board has a piece, print the type ID using
            # a different color, and then a right bracket
            else:
                # If the piece is red, print a red type ID
                if board[(num, 10)].get_contains().get_color() == "red":
                    print("\033[0;31;48m" +
                        board[(num, 10)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

                # If the piece is black, print a teal type ID
                if board[(num, 10)].get_contains().get_color() == "black":
                    print("\033[0;36;48m" +
                          board[(num, 10)].get_contains().get_type_id(),
                          end = "")
                    print("\033[0;29;48m]", end = "")

        print("\033[0;30;47m 10", end="")   # Row label at end
        print("\033[0;29;48m", end="\n")

        # Print the first footer row
        print("\033[0;30;47m    1", end = "  ")
        print("\033[0;30;47m2", end = "  ")
        print("\033[0;30;47m3", end = "  ")
        print("\033[0;90;47m4", end = "  ")
        print("\033[0;90;47m5", end = "  ")
        print("\033[0;90;47m6", end = "  ")
        print("\033[0;30;47m7", end = "  ")
        print("\033[0;30;47m8", end = "  ")
        print("\033[0;30;47m9", end = "    ")
        print("\033[0;97;30m")

        # Print the second footer row
        print("\033[0;30;47m    a", end = "  ")
        print("\033[0;30;47mb", end = "  ")
        print("\033[0;30;47mc", end = "  ")
        print("\033[0;90;47md", end = "  ")
        print("\033[0;90;47me", end = "  ")
        print("\033[0;90;47mf", end = "  ")
        print("\033[0;30;47mg", end = "  ")
        print("\033[0;30;47mh", end = "  ")
        print("\033[0;30;47mi", end = "    ")
        print("\033[0;97;30m")

    @staticmethod
    def quantify_location(location_str):
        """
        Take as a parameter a string representing a location on the board in
        algebraic notation (e.g. 'c1'); convert the letter into a number; and
        return a tuple representing the location in (column, row) format using
        the digits 1-10.
        """
        # If the length of the location string is 3, since the first character
        # must be a single letter, the second and third characters must make
        # up "10"
        if len(location_str) == 3:
            number_int = 10

        # Get the individual characters of the string parameter
        letter_char = location_str[0]
        number_char = location_str[1]

        if len(location_str) == 2:
            number_int = int(number_char)

        if letter_char == 'a':
            return (1, number_int)

        if letter_char == 'b':
            return (2, number_int)

        if letter_char == 'c':
            return (3, number_int)

        if letter_char == 'd':
            return (4, number_int)

        if letter_char == 'e':
            return (5, number_int)

        if letter_char == 'f':
            return (6, number_int)

        if letter_char == 'g':
            return (7, number_int)

        if letter_char == 'h':
            return (8, number_int)

        if letter_char == 'i':
            return (9, number_int)


class Board:
    """
    Represent the game board, implemented as a dictionary whose keys are the
    possible coordinates on the board, and whose values are point objects.
    The init method sets up the starting pieces on the board.
    """
    def __init__(self):
        """
        Create a Board object. The board is represented by a dictionary whose
        keys are the board coordinates as tuples and whose values are point
        objects.
        """
        self._board = {

            # Initialize row 1
            (1, 1): Point(1, 1, Chariot("red", 1, 1)),
            (2, 1): Point(2, 1, Horse("red", 2, 1)),
            (3, 1): Point(3, 1, Elephant("red", 3, 1)),
            (4, 1): Point(4, 1, Advisor("red", 4, 1)),
            (5, 1): Point(5, 1, General("red", 5, 1)),
            (6, 1): Point(6, 1, Advisor("red", 6, 1)),
            (7, 1): Point(7, 1, Elephant("red", 7, 1)),
            (8, 1): Point(8, 1, Horse("red", 8, 1)),
            (9, 1): Point(9, 1, Chariot("red", 9, 1)),

            # Initialize row 2
            (1, 2): Point(1, 2),
            (2, 2): Point(2, 2),
            (3, 2): Point(3, 2),
            (4, 2): Point(4, 2),
            (5, 2): Point(5, 2),
            (6, 2): Point(6, 2),
            (7, 2): Point(7, 2),
            (8, 2): Point(8, 2),
            (9, 2): Point(9, 2),

            # Initialize row 3
            (1, 3): Point(1, 3),
            (2, 3): Point(2, 3, Cannon("red", 2, 3)),
            (3, 3): Point(3, 3),
            (4, 3): Point(4, 3),
            (5, 3): Point(5, 3),
            (6, 3): Point(6, 3),
            (7, 3): Point(7, 3),
            (8, 3): Point(8, 3, Cannon("red", 8, 3)),
            (9, 3): Point(9, 3),

            # Initialize row 4
            (1, 4): Point(1, 4, Soldier("red", 1, 4)),
            (2, 4): Point(2, 4),
            (3, 4): Point(3, 4, Soldier("red", 3, 4)),
            (4, 4): Point(4, 4),
            (5, 4): Point(5, 4, Soldier("red", 5, 4)),
            (6, 4): Point(6, 4),
            (7, 4): Point(7, 4, Soldier("red", 7, 4)),
            (8, 4): Point(8, 4),
            (9, 4): Point(9, 4, Soldier("red", 9, 4)),

            # Initialize row 5
            (1, 5): Point(1, 5),
            (2, 5): Point(2, 5),
            (3, 5): Point(3, 5),
            (4, 5): Point(4, 5),
            (5, 5): Point(5, 5),
            (6, 5): Point(6, 5),
            (7, 5): Point(7, 5),
            (8, 5): Point(8, 5),
            (9, 5): Point(9, 5),

            # Initialize row 6
            (1, 6): Point(1, 6),
            (2, 6): Point(2, 6),
            (3, 6): Point(3, 6),
            (4, 6): Point(4, 6),
            (5, 6): Point(5, 6),
            (6, 6): Point(6, 6),
            (7, 6): Point(7, 6),
            (8, 6): Point(8, 6),
            (9, 6): Point(9, 6),

            # Initialize row 7
            (1, 7): Point(1, 7, Soldier("black", 1, 7)),
            (2, 7): Point(2, 7),
            (3, 7): Point(3, 7, Soldier("black", 3, 7)),
            (4, 7): Point(4, 7),
            (5, 7): Point(5, 7, Soldier("black", 5, 7)),
            (6, 7): Point(6, 7),
            (7, 7): Point(7, 7, Soldier("black", 7, 7)),
            (8, 7): Point(8, 7),
            (9, 7): Point(9, 7, Soldier("black", 9, 7)),

            # Initialize row 8
            (1, 8): Point(1, 8),
            (2, 8): Point(2, 8, Cannon("black", 2, 8)),
            (3, 8): Point(3, 8),
            (4, 8): Point(4, 8),
            (5, 8): Point(5, 8),
            (6, 8): Point(6, 8),
            (7, 8): Point(7, 8),
            (8, 8): Point(8, 8, Cannon("black", 8, 8)),
            (9, 8): Point(9, 8),

            # Initialize row 9
            (1, 9): Point(1, 9),
            (2, 9): Point(2, 9),
            (3, 9): Point(3, 9),
            (4, 9): Point(4, 9),
            (5, 9): Point(5, 9),
            (6, 9): Point(6, 9),
            (7, 9): Point(7, 9),
            (8, 9): Point(8, 9),
            (9, 9): Point(9, 9),

            # Initialize row 10
            (1, 10): Point(1, 10, Chariot("black", 1, 10)),
            (2, 10): Point(2, 10, Horse("black", 2, 10)),
            (3, 10): Point(3, 10, Elephant("black", 3, 10)),
            (4, 10): Point(4, 10, Advisor("black", 4, 10)),
            (5, 10): Point(5, 10, General("black", 5, 10)),
            (6, 10): Point(6, 10, Advisor("black", 6, 10)),
            (7, 10): Point(7, 10, Elephant("black", 7, 10)),
            (8, 10): Point(8, 10, Horse("black", 8, 10)),
            (9, 10): Point(9, 10, Chariot("black", 9, 10))
        }

        # Initialize each point's _shadowed_by data member
        self.update_points_shadows()

    def get_board(self):
        """
        Return the board data member.
        """
        return self._board

    def print_pieces_shadows(self):
        """
        For every piece on the board, print out what points it is shadowing.
        """
        for row in range(1, 11):       # Outer loop goes through each row
            for col in range(1, 10):   # Inner loop goes through each column
                if self._board[(col, row)].get_contains() is not None:
                    piece = self._board[(col, row)].get_contains()
                    print(piece.get_color(), piece.get_type_id(), "@" + "(" +
                          str(col) + "," + str(row) + ") " +
                          "shadows:", piece.get_shadows())
        print()

    def print_points_shadows(self):
        """
        For every point on the board, print out what pieces it is shadowed by.
        """
        for row in range(1, 11):       # Outer loop goes through each row
            for col in range(1, 10):   # Inner loop goes through each column
                print("(" + str(col) + "," + str(row) + ") " +
                      "is shadowed by: ", end='')
                for piece in self._board[(col, row)].get_shadowed_by():
                    print(piece.get_color(), piece.get_type_id(), "@" + "(" +
                          str(piece.get_col()) + "," + str(piece.get_row()) +
                          "), ", end='')
                print()

    def update_points_shadows(self):
        """
        For every point on the board, update its list of pieces it is being
        shadowed by.
        """
        # Clear every point's list of pieces it is shadowed by
        for coord in self._board:
            self._board[coord].clear_shadowed_by()

        # Update every point's list of pieces it is shadowed by
        # Check every point on the board
        for coordinate in self._board:
            point = self._board[coordinate]

            # If the point has a piece
            if point.get_contains() is not None:
                piece = point.get_contains()

                # Update the point's _shadowed_by data member
                for shadowed_coordinate in piece.get_shadows():
                    self._board[shadowed_coordinate].add_shadowed_by(piece)


class Point:
    """
    Represent a point on the board. Has various getter and setter methods for
    retrieving and updating the column position, row position, what piece
    (if any) the point holds, and what pieces (if any) are shadowing the
    point.
    """
    def __init__(self, col, row, piece=None):
        """
        Take as parameters a column position, row position, and a piece
        (optional) to create a point object. If no piece is provided, the
        point contains None by default.
        """
        self._col = col
        self._row = row
        self._contains = piece
        self._shadowed_by = []   # Pieces that shadow the point

    def get_col(self):
        """
        Return the column position of the point.
        """
        return self._col

    def get_row(self):
        """
        Return the row position of the point.
        """
        return self._row

    def get_contains(self):
        """
        Return what piece (if any) the point contains.
        """
        return self._contains

    def set_contains(self, piece):
        """
        Update what the point holds (a different piece or None).
        """
        self._contains = piece

    def get_shadowed_by(self):
        """
        Return what pieces (if any) are shadowing the point.
        """
        return self._shadowed_by

    def add_shadowed_by(self, piece):
        """
        Take as a parameter a piece object and add that piece to the list
        keeping track of what pieces are shadowing the point.
        """
        self._shadowed_by.append(piece)

    def clear_shadowed_by(self):
        """
        Delete all pieces from the list keeping track of what pieces are
        shadowing the point.
        """
        self._shadowed_by.clear()


class Piece:
    """
    Represent a game piece. This class is the superclass of General, Advisor,
    Elephant, Horse, Chariot, Cannon, and Soldier. Has various getter and
    setter methods for retrieving and updating the piece's color, column
    position, row position, type ID, and list of coordinates (tuples) that it
    is shadowing.
    """
    def __init__(self, color, col, row):
        """
        Take as parameters the piece's color, column position, and row
        position and create a piece object with the corresponding data members
        initialized, in addition to the piece's type ID and the list of
        coordinates that it is shadowing.
        """
        self._color = color
        self._col = col
        self._row = row
        self._type_id = None  # Identify the piece's type via a single letter
        self._shadows = []    # Track coordinates that the piece can move to

    def get_color(self):
        """
        Return the color of the piece.
        """
        return self._color

    def get_col(self):
        """
        Return the column position of the piece.
        """
        return self._col

    def set_col(self, col_pos):
        """
        Update the column position of the piece.
        """
        self._col = col_pos

    def get_row(self):
        """
        Return the row position of the piece.
        """
        return self._row

    def set_row(self, row_pos):
        """
        Update the row position of the piece.
        """
        self._row = row_pos

    def get_type_id(self):
        """
        Return the type ID of the piece.
        """
        return self._type_id

    def get_shadows(self):
        """
        Return the list of coordinates (if any) that the piece is shadowing.
        """
        return self._shadows


class General(Piece):
    """
    Represent a general (i.e. king) piece. This class is a subclass of Piece.
    """
    def __init__(self, color, col, row):
        """
        Take as parameters the general's color, column position, and row
        position to create a General object. Initialize the corresponding
        data members, as well as the type ID.
        """
        super().__init__(color, col, row)
        self._type_id = 'G'                # First letter of "General"

        # Initialize the list of points that the general currently shadows.
        # If any adjacent orthogonal points are within the board and within
        # the palace, add them to the general's _shadows data member.

        # If the general is red
        if color == "red":
            self._shadows.append((col, row + 1))

        # If the general is black
        if self._color == "black":
            self._shadows.append((col, row - 1))

    def update_shadows(self, board):
        """
        Take as a parameter the current board and update the general's list of
        coordinates that it is shadowing.
        """
        self._shadows.clear()
        col = self._col
        row = self._row

        # Check for possible points that the red general can move to
        if self._color == "red":
            # Check the north orthogonal point
            if 1 <= (row - 1) <= 3:
                if board[(col, row - 1)].get_contains() is None:
                    self._shadows.append((col, row - 1))

                # If there is a piece on the point, check its color
                else:
                    piece = board[(col, row - 1)].get_contains()
                    if piece.get_color() != self._color:
                        self._shadows.append((col, row - 1))

            # Check the south orthogonal point
            if 1 <= (row + 1) <= 3:
                if board[(col, row + 1)].get_contains() is None:
                    self._shadows.append((col, row + 1))

                # If there is a piece on the point, check its color
                else:
                    piece = board[(col, row + 1)].get_contains()
                    if piece.get_color() != self._color:
                        self._shadows.append((col, row + 1))

            # Check the east orthogonal point
            if 4 <= (col + 1) <= 6:
                if board[(col + 1, row)].get_contains() is None:
                    self._shadows.append((col + 1, row))

                # If there is a piece on the point, check its color
                else:
                    piece = board[(col + 1, row)].get_contains()
                    if piece.get_color() != self._color:
                        self._shadows.append((col + 1, row))

            # Check the west orthogonal point
            if 4 <= (col - 1) <= 6:
                if board[(col - 1, row)].get_contains() is None:
                    self._shadows.append((col - 1, row))

                # If there is a piece on the point, check its color
                else:
                    piece = board[(col - 1, row)].get_contains()
                    if piece.get_color() != self._color:
                        self._shadows.append((col - 1, row))

            # Check for the "flying general" condition:
            # Get the black general's column and row positions
            black_gen_col = None
            black_gen_row = None
            is_file_clear = True   # Assume True unless proven otherwise

            # Check every point on the board
            for coord in board:

                # If the point has a piece
                if board[coord].get_contains() is not None:
                    piece = board[coord].get_contains()

                    # If the piece is black
                    if piece.get_color() == "black":

                        # If the piece is a general
                        if piece.get_type_id() == 'G':
                            black_gen_col = piece.get_col()
                            black_gen_row = piece.get_row()

            # If the two generals are in the same column
            if self._col == black_gen_col:

                # Check for pieces in the rows between the generals
                for row_num in range(self._row + 1, black_gen_row):
                    # If there is a piece
                    if board[(self._col, row_num)].get_contains() is not None:
                        is_file_clear = False

                # If there are no intervening pieces between the generals
                if is_file_clear:
                    # Add all points between the generals, as well as the
                    # black general's point, to the red general's _shadows
                    # data member
                    for row_num in range(self._row + 1, black_gen_row + 1):
                        self._shadows.append((self._col, row_num))

        # Check for possible points that the black general can move to
        if self._color == "black":
            # Check the north orthogonal point
            if 8 <= (row - 1) <= 10:
                if board[(col, row - 1)].get_contains() is None:
                    self._shadows.append((col, row - 1))

                # If there is a piece on the point, check its color
                else:
                    piece = board[(col, row - 1)].get_contains()
                    if piece.get_color() != self._color:
                        self._shadows.append((col, row - 1))

            # Check the south orthogonal point
            if 8 <= (row + 1) <= 10:
                if board[(col, row + 1)].get_contains() is None:
                    self._shadows.append((col, row + 1))

                # If there is a piece on the point, check its color
                else:
                    piece = board[(col, row + 1)].get_contains()
                    if piece.get_color() != self._color:
                        self._shadows.append((col, row + 1))

            # Check the east orthogonal point
            if 4 <= (col + 1) <= 6:
                if board[(col + 1, row)].get_contains() is None:
                    self._shadows.append((col + 1, row))

                # If there is a piece on the point, check its color
                else:
                    piece = board[(col + 1, row)].get_contains()
                    if piece.get_color() != self._color:
                        self._shadows.append((col + 1, row))

            # Check the west orthogonal point
            if 4 <= (col - 1) <= 6:
                if board[(col - 1, row)].get_contains() is None:
                    self._shadows.append((col - 1, row))

                # If there is a piece on the point, check its color
                else:
                    piece = board[(col - 1, row)].get_contains()
                    if piece.get_color() != self._color:
                        self._shadows.append((col - 1, row))

            # Check for the "flying general" condition:
            # Get the red general's column and row positions
            red_gen_col = None
            red_gen_row = None
            is_file_clear = True   # Assume True unless proven otherwise

            # Check every point on the board
            for coord in board:

                # If the point has a piece
                if board[coord].get_contains() is not None:
                    piece = board[coord].get_contains()

                    # If the piece is red
                    if piece.get_color() == "red":

                        # If the piece is a general
                        if piece.get_type_id() == 'G':
                            red_gen_col = piece.get_col()
                            red_gen_row = piece.get_row()

            # If the two generals are in the same column
            if self._col == red_gen_col:

                # Check for pieces in the rows between the generals
                for row_num in range(red_gen_row + 1, self._row):
                    # If there is a piece
                    if board[(self._col, row_num)].get_contains() is not None:
                        is_file_clear = False

                # If there are no intervening pieces between the generals
                if is_file_clear:
                    # Add all points between the generals, as well as the red
                    # general's point, to the black general's _shadows data
                    # member
                    for row_num in range(red_gen_row, self._row):
                        self._shadows.append((self._col, row_num))


class Advisor(Piece):
    """
    Represent an advisor piece. This class is a subclass of Piece.
    """
    def __init__(self, color, col, row):
        """
        Take as parameters and initialize the advisor's color, column
        position, and row position to create an Advisor object. Initialize
        the corresponding data members, as well as the type ID.
        """
        super().__init__(color, col, row)
        self._type_id = 'A'                # First letter of "Advisor"

        # Initialize the list of coordinates that the advisor currently
        # shadows. If any points diagonal to the advisor are within the board
        # and within the palace, add them to the advisor's _shadows data
        # member.

        # If the advisor is red
        if color == "red":
            # Check the northeast diagonal
            if (4 <= (col + 1) <= 6) and (1 <= (row - 1) <= 3):
                self._shadows.append((col + 1, row - 1))

            # Check the southeast diagonal
            if (4 <= (col + 1) <= 6) and (1 <= (row + 1) <= 3):
                self._shadows.append((col + 1, row + 1))

            # Check the southwest diagonal
            if (4 <= (col - 1) <= 6) and (1 <= (row + 1) <= 3):
                self._shadows.append((col - 1, row + 1))

            # Check the northwest diagonal
            if (4 <= (col - 1) <= 6) and (1 <= (row - 1) <= 3):
                self._shadows.append((col - 1, row - 1))

        # If the advisor is black
        if color == "black":
            # Check the northeast diagonal
            if (4 <= (col + 1) <= 6) and (8 <= (row - 1) <= 10):
                self._shadows.append((col + 1, row - 1))

            # Check the southeast diagonal
            if (4 <= (col + 1) <= 6) and (8 <= (row + 1) <= 10):
                self._shadows.append((col + 1, row + 1))

            # Check the southwest diagonal
            if (4 <= (col - 1) <= 6) and (8 <= (row + 1) <= 10):
                self._shadows.append((col - 1, row + 1))

            # Check the northwest diagonal
            if (4 <= (col - 1) <= 6) and (8 <= (row - 1) <= 10):
                self._shadows.append((col - 1, row - 1))

    def update_shadows(self, board):
        """
        Take as a parameter the current board and update the advisor's list of
        coordinates that it is shadowing.
        """
        self._shadows.clear()
        col = self._col
        row = self._row

        # Check for possible points that the red advisor can move to
        if self._color == "red":

            # Check the northeast diagonal
            if (4 <= (col + 1) <= 6) and (1 <= (row - 1) <= 3):

                # If the point is empty
                if board[(col + 1, row - 1)].get_contains() is None:
                    self._shadows.append((col + 1, row - 1))

                # If the point has a piece
                else:
                    piece = board[(col + 1, row - 1)].get_contains()

                    # If the piece belongs to the opponent
                    if piece.get_color() != self.get_color():
                        self._shadows.append((col + 1, row - 1))

            # Check the southeast diagonal
            if (4 <= (col + 1) <= 6) and (1 <= (row + 1) <= 3):

                # If the point is empty
                if board[(col + 1, row + 1)].get_contains() is None:
                    self._shadows.append((col + 1, row + 1))

                # If the point has a piece
                else:
                    piece = board[(col + 1, row + 1)].get_contains()

                    # If the piece belongs to the opponent
                    if piece.get_color() != self.get_color():
                        self._shadows.append((col + 1, row + 1))

            # Check the southwest diagonal
            if (4 <= (col - 1) <= 6) and (1 <= (row + 1) <= 3):

                # If the point is empty
                if board[(col - 1, row + 1)].get_contains() is None:
                    self._shadows.append((col - 1, row + 1))

                # If the point has a piece
                else:
                    piece = board[(col - 1, row + 1)].get_contains()

                    # If the piece belongs to the opponent
                    if piece.get_color() != self.get_color():
                        self._shadows.append((col - 1, row + 1))

            # Check the northwest diagonal
            if (4 <= (col - 1) <= 6) and (1 <= (row - 1) <= 3):

                # If the point is empty
                if board[(col - 1, row - 1)].get_contains() is None:
                    self._shadows.append((col - 1, row - 1))

                # If the point has a piece
                else:
                    piece = board[(col - 1, row - 1)].get_contains()

                    # If the piece belongs to the opponent
                    if piece.get_color() != self.get_color():
                        self._shadows.append((col - 1, row - 1))

        # Check for possible points that the black advisor can move to
        if self._color == "black":

            # Check the northeast diagonal
            if (4 <= (col + 1) <= 6) and (8 <= (row - 1) <= 10):

                # If the point is empty
                if board[(col + 1, row - 1)].get_contains() is None:
                    self._shadows.append((col + 1, row - 1))

                # If the point has a piece
                else:
                    piece = board[(col + 1, row - 1)].get_contains()

                    # If the piece belongs to the opponent
                    if piece.get_color() != self.get_color():
                        self._shadows.append((col + 1, row - 1))

            # Check the southeast diagonal
            if (4 <= (col + 1) <= 6) and (8 <= (row + 1) <= 10):

                # If the point is empty
                if board[(col + 1, row + 1)].get_contains() is None:
                    self._shadows.append((col + 1, row + 1))

                # If the point has a piece
                else:
                    piece = board[(col + 1, row + 1)].get_contains()

                    # If the piece belongs to the opponent
                    if piece.get_color() != self.get_color():
                        self._shadows.append((col + 1, row + 1))

            # Check the southwest diagonal
            if (4 <= (col - 1) <= 6) and (8 <= (row + 1) <= 10):

                # If the point is empty
                if board[(col - 1, row + 1)].get_contains() is None:
                    self._shadows.append((col - 1, row + 1))

                # If the point has a piece
                else:
                    piece = board[(col - 1, row + 1)].get_contains()

                    # If the piece belongs to the opponent
                    if piece.get_color() != self.get_color():
                        self._shadows.append((col - 1, row + 1))

            # Check the northwest diagonal
            if (4 <= (col - 1) <= 6) and (8 <= (row - 1) <= 10):

                # If the point is empty
                if board[(col - 1, row - 1)].get_contains() is None:
                    self._shadows.append((col - 1, row - 1))

                # If the point has a piece
                else:
                    piece = board[(col - 1, row - 1)].get_contains()

                    # If the piece belongs to the opponent
                    if piece.get_color() != self.get_color():
                        self._shadows.append((col - 1, row - 1))


class Elephant(Piece):
    """
    Represent an elephant piece. This class is a subclass of Piece.
    """
    def __init__(self, color, col, row):
        """
        Take as parameters the elephant's color, column position, and row
        position to create an Elephant object. Initialize the corresponding
        data members, as well as the type ID.
        """
        super().__init__(color, col, row)
        self._type_id = 'E'                # First letter of "Elephant"

        # Initialize the list of coordinates that the elephant is shadowing

        # Check northeast two points diagonally
        if (1 <= (col + 2) <= 9) and (1 <= (row - 2) <= 10):
            self._shadows.append((col + 2, row - 2))

        # Check southeast two points diagonally
        if (1 <= (col + 2) <= 9) and (1 <= (row + 2) <= 10):
            self._shadows.append((col + 2, row + 2))

        # Check southwest two points diagonally
        if (1 <= (col - 2) <= 9) and (1 <= (row + 2) <= 10):
            self._shadows.append((col - 2, row + 2))

        # Check northwest two points diagonally
        if (1 <= (col - 2) <= 9) and (1 <= (row - 2) <= 10):
            self._shadows.append((col - 2, row - 2))

    def update_shadows(self, board):
        """
        Take as a parameter the current board and update the elephant's list
        of coordinates that it is shadowing.
        """
        self._shadows.clear()
        col = self._col
        row = self._row

        # Check for possible points that the red elephant can move to
        if self._color == "red":

            # Check northeast one point diagonally for an intervening piece
            if (1 <= (col + 1) <= 9) and (1 <= (row - 1) <= 5):

                # If there is no intervening piece
                if board[(col + 1, row - 1)].get_contains() is None:

                    # Check northeast two points diagonally
                    if (1 <= (col + 2) <= 9) and (1 <= (row - 2) <= 5):

                        # If the point is empty
                        if board[(col + 2, row - 2)].get_contains() is None:
                            self._shadows.append((col + 2, row - 2))

                        # If the point has a piece
                        else:
                            piece = board[(col + 2, row - 2)].get_contains()

                            # If the piece belongs to the opponent
                            if piece.get_color() != self.get_color():
                                self._shadows.append((col + 2, row - 2))

            # Check southeast one point diagonally for an intervening piece
            if (1 <= (col + 1) <= 9) and (1 <= (row + 1) <= 5):

                # If there is no intervening piece
                if board[(col + 1, row + 1)].get_contains() is None:

                    # Check southeast two points diagonally
                    if (1 <= (col + 2) <= 9) and (1 <= (row + 2) <= 5):

                        # If the point is empty
                        if board[(col + 2, row + 2)].get_contains() is None:
                            self._shadows.append((col + 2, row + 2))

                        # If the point has a piece
                        else:
                            piece = board[(col + 2, row + 2)].get_contains()

                            # If the piece belongs to the opponent
                            if piece.get_color() != self.get_color():
                                self._shadows.append((col + 2, row + 2))

            # Check southwest one point diagonally for an intervening piece
            if (1 <= (col - 1) <= 9) and (1 <= (row + 1) <= 5):

                # If there is no intervening piece
                if board[(col - 1, row + 1)].get_contains() is None:

                    # Check southwest two points diagonally
                    if (1 <= (col - 2) <= 9) and (1 <= (row + 2) <= 5):

                        # If the point is empty
                        if board[(col - 2, row + 2)].get_contains() is None:
                            self._shadows.append((col - 2, row + 2))

                        # If the point has a piece
                        else:
                            piece = board[(col - 2, row + 2)].get_contains()

                            # If the piece belongs to the opponent
                            if piece.get_color() != self.get_color():
                                self._shadows.append((col - 2, row + 2))

            # Check northwest one point diagonally for an intervening piece
            if (1 <= (col - 1) <= 9) and (1 <= (row - 1) <= 5):

                # If there is no intervening piece
                if board[(col - 1, row - 1)].get_contains() is None:

                    # Check northwest two points diagonally
                    if (1 <= (col - 2) <= 9) and (1 <= (row - 2) <= 5):

                        # If the point is empty
                        if board[(col - 2, row - 2)].get_contains() is None:
                            self._shadows.append((col - 2, row - 2))

                        # If the point has a piece
                        else:
                            piece = board[(col - 2, row - 2)].get_contains()

                            # If the piece belongs to the opponent
                            if piece.get_color() != self.get_color():
                                self._shadows.append((col - 2, row - 2))

        # Check for possible points that the black elephant can move to
        if self._color == "black":

            # Check northeast one point diagonally for an intervening piece
            if (1 <= (col + 1) <= 9) and (6 <= (row - 1) <= 10):

                # If there is no intervening piece
                if board[(col + 1, row - 1)].get_contains() is None:

                    # Check northeast two points diagonally
                    if (1 <= (col + 2) <= 9) and (6 <= (row - 2) <= 10):

                        # If the point is empty
                        if board[(col + 2, row - 2)].get_contains() is None:
                            self._shadows.append((col + 2, row - 2))

                        # If the point has a piece
                        else:
                            piece = board[(col + 2, row - 2)].get_contains()

                            # If the piece belongs to the opponent
                            if piece.get_color() != self.get_color():
                                self._shadows.append((col + 2, row - 2))

            # Check southeast one point diagonally for an intervening piece
            if (1 <= (col + 1) <= 9) and (6 <= (row + 1) <= 10):

                # If there is no intervening piece
                if board[(col + 1, row + 1)].get_contains() is None:

                    # Check southeast two points diagonally
                    if (1 <= (col + 2) <= 9) and (6 <= (row + 2) <= 10):

                        # If the point is empty
                        if board[(col + 2, row + 2)].get_contains() is None:
                            self._shadows.append((col + 2, row + 2))

                        # If the point has a piece
                        else:
                            piece = board[(col + 2, row + 2)].get_contains()

                            # If the piece belongs to the opponent
                            if piece.get_color() != self.get_color():
                                self._shadows.append((col + 2, row + 2))

            # Check southwest one point diagonally for an intervening piece
            if (1 <= (col - 1) <= 9) and (6 <= (row + 1) <= 10):

                # If there is no intervening piece
                if board[(col - 1, row + 1)].get_contains() is None:

                    # Check southwest two points diagonally
                    if (1 <= (col - 2) <= 9) and (6 <= (row + 2) <= 10):

                        # If the point is empty
                        if board[(col - 2, row + 2)].get_contains() is None:
                            self._shadows.append((col - 2, row + 2))

                        # If the point has a piece
                        else:
                            piece = board[(col - 2, row + 2)].get_contains()

                            # If the piece belongs to the opponent
                            if piece.get_color() != self.get_color():
                                self._shadows.append((col - 2, row + 2))

            # Check northwest one point diagonally for an intervening piece
            if (1 <= (col - 1) <= 9) and (6 <= (row - 1) <= 10):

                # If there is no intervening piece
                if board[(col - 1, row - 1)].get_contains() is None:

                    # Check northwest two points diagonally
                    if (1 <= (col - 2) <= 9) and (6 <= (row - 2) <= 10):

                        # If the point is empty
                        if board[(col - 2, row - 2)].get_contains() is None:
                            self._shadows.append((col - 2, row - 2))

                        # If the point has a piece
                        else:
                            piece = board[(col - 2, row - 2)].get_contains()

                            # If the piece belongs to the opponent
                            if piece.get_color() != self.get_color():
                                self._shadows.append((col - 2, row - 2))


class Horse(Piece):
    """
    Represent a horse piece. This class is a subclass of Piece.
    """
    def __init__(self, color, col, row):
        """
        Take as parameters the horse's color, column position, and row
        position. Initialize the corresponding data members, as well as the
        type ID.
        """
        super().__init__(color, col, row)
        self._type_id = 'H'                # First letter of "Horse"

        # Initialize the list of coordinates that the horse is shadowing

        # Check northeast one point orthogonally and one point diagonally
        if (1 <= (col + 1) <= 9) and (1 <= (row - 2) <= 10):
            self._shadows.append((col + 1, row - 2))

        # Check southeast one point orthogonally and one point diagonally
        if (1 <= (col + 1) <= 9) and (1 <= (row + 2) <= 10):
            self._shadows.append((col + 1, row + 2))

        # Check southwest one point orthogonally and one point diagonally
        if (1 <= (col - 1) <= 9) and (1 <= (row + 2) <= 10):
            self._shadows.append((col - 1, row + 2))

        # Check northwest one point orthogonally and one point diagonally
        if (1 <= (col - 1) <= 9) and (1 <= (row - 2) <= 10):
            self._shadows.append((col - 1, row - 2))

    def update_shadows(self, board):
        """
        Take as a parameter the current board and update the horse's list of
        coordinates that it is shadowing.
        """
        self._shadows.clear()
        col = self._col
        row = self._row

        # Check for possible points that the horse can move to:

        # Check the north orthogonal point
        if 1 <= (row - 1) <= 10:

            # If the north orthogonal point is empty
            if board[(col, row - 1)].get_contains() is None:

                # From the north orthogonal point, check the northwest diagonal
                if (1 <= (col - 1) <= 9) and (1 <= (row - 2) <= 10):

                    # If the north-northwest point is empty
                    if board[(col - 1, row - 2)].get_contains() is None:
                        self._shadows.append((col - 1, row - 2))

                    # If the north-northwest point has a piece
                    else:
                        piece = board[(col - 1, row - 2)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self.get_color():
                            self._shadows.append((col - 1, row - 2))

                # From the north orthogonal point, check the northeast diagonal
                if (1 <= (col + 1) <= 9) and (1 <= (row - 2) <= 10):

                    # If the north-northeast point is empty
                    if board[(col + 1, row - 2)].get_contains() is None:
                        self._shadows.append((col + 1, row - 2))

                    # If the north-northeast point has a piece
                    else:
                        piece = board[(col + 1, row - 2)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self.get_color():
                            self._shadows.append((col + 1, row - 2))

        # Check the east orthogonal point
        if 1 <= (col + 1) <= 9:

            # If the east orthogonal point is empty
            if board[(col + 1, row)].get_contains() is None:

                # From the east orthogonal point, check the northeast diagonal
                if (1 <= (col + 2) <= 9) and (1 <= (row - 1) <= 10):

                    # If the east-northeast point is empty
                    if board[(col + 2, row - 1)].get_contains() is None:
                        self._shadows.append((col + 2, row - 1))

                    # If the east-northeast point has a piece
                    else:
                        piece = board[(col + 2, row - 1)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self.get_color():
                            self._shadows.append((col + 2, row - 1))

                # From the east orthogonal point, check the southeast diagonal
                if (1 <= (col + 2) <= 9) and (1 <= (row + 1) <= 10):

                    # If the east-southeast point is empty
                    if board[(col + 2, row + 1)].get_contains() is None:
                        self._shadows.append((col + 2, row + 1))

                    # If the east-southeast point has a piece
                    else:
                        piece = board[(col + 2, row + 1)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self.get_color():
                            self._shadows.append((col + 2, row + 1))

        # Check the south orthogonal point
        if 1 <= (row + 1) <= 10:

            # If the south orthogonal point is empty
            if board[(col, row + 1)].get_contains() is None:

                # From the south orthogonal point, check the southeast diagonal
                if (1 <= (col + 1) <= 9) and (1 <= (row + 2) <= 10):

                    # If the south-southeast point is empty
                    if board[(col + 1, row + 2)].get_contains() is None:
                        self._shadows.append((col + 1, row + 2))

                    # If the south-southeast point has a piece
                    else:
                        piece = board[(col + 1, row + 2)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self.get_color():
                            self._shadows.append((col + 1, row + 2))

                # From the south orthogonal point, check the southwest diagonal
                if (1 <= (col - 1) <= 9) and (1 <= (row + 2) <= 10):

                    # If the south-southwest point is empty
                    if board[(col - 1, row + 2)].get_contains() is None:
                        self._shadows.append((col - 1, row + 2))

                    # If the south-southwest point has a piece
                    else:
                        piece = board[(col - 1, row + 2)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self.get_color():
                            self._shadows.append((col - 1, row + 2))

        # Check the west orthogonal point
        if 1 <= (col - 1) <= 9:

            # If the west orthogonal point is empty
            if board[(col - 1, row)].get_contains() is None:

                # From the west orthogonal point, check the southwest diagonal
                if (1 <= (col - 2) <= 9) and (1 <= (row + 1) <= 10):

                    # If the west-southwest point is empty
                    if board[(col - 2, row + 1)].get_contains() is None:
                        self._shadows.append((col - 2, row + 1))

                    # If the west-southwest point has a piece
                    else:
                        piece = board[(col - 2, row + 1)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self.get_color():
                            self._shadows.append((col - 2, row + 1))

                # From the west orthogonal point, check the northwest diagonal
                if (1 <= (col - 2) <= 9) and (1 <= (row - 1) <= 10):

                    # If the west-northwest point is empty
                    if board[(col - 2, row - 1)].get_contains() is None:
                        self._shadows.append((col - 2, row - 1))

                    # If the west-northwest point has a piece
                    else:
                        piece = board[(col - 2, row - 1)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self.get_color():
                            self._shadows.append((col - 2, row - 1))


class Chariot(Piece):
    """
    Represent a chariot piece. This class is a subclass of Piece.
    """
    def __init__(self, color, col, row):
        """
        Take as parameters the chariot's color, column position, and row
        position to create a Chariot object. Initialize the corresponding
        data members, as well as the type ID.
        """
        super().__init__(color, col, row)
        self._type_id = 'C'                # First letter of "Chariot"

        # Initialize the list of coordinates that the chariot is shadowing
        if self._color == "red":
            self._shadows.append((col, row + 1))
            self._shadows.append((col, row + 2))

        if self._color == "black":
            self._shadows.append((col, row - 1))
            self._shadows.append((col, row - 2))

    def update_shadows(self, board):
        """
        Take as a parameter the current board and update the chariot's list of
        coordinates that it is shadowing.
        """
        self._shadows.clear()
        col = self._col
        row = self._row

        # Check for possible points that the chariot can move to:

        # Check the north piece(s)
        row_offset = 1

        # Check if the next north piece is within the bounds of the board
        while 1 <= (row - row_offset) <= 10:
            # If the point is empty
            if board[(col, row - row_offset)].get_contains() is None:
                self._shadows.append((col, row - row_offset))
                row_offset += 1
                continue

            else:   # If the point has a piece
                piece = board[(col, row - row_offset)].get_contains()

                # If the piece belongs to the opponent
                if piece.get_color() != self._color:
                    self._shadows.append((col, row - row_offset))
                    break

                else:   # If the piece is the current player's
                    break

        # Check the south piece(s)
        row_offset = 1

        # Check if the next south piece is within the bounds of the board
        while 1 <= (row + row_offset) <= 10:
            # If the point is empty
            if board[(col, row + row_offset)].get_contains() is None:
                self._shadows.append((col, row + row_offset))
                row_offset += 1
                continue

            else:   # If the point has a piece
                piece = board[(col, row + row_offset)].get_contains()

                # If the piece belongs to the opponent
                if piece.get_color() != self._color:
                    self._shadows.append((col, row + row_offset))
                    break

                else:   # If the piece is the current player's
                    break

        # Check the east piece(s)
        col_offset = 1

        # Check if the next east piece is within the bounds of the board
        while 1 <= (col + col_offset) <= 9:
            # If the point is empty
            if board[(col + col_offset, row)].get_contains() is None:
                self._shadows.append((col + col_offset, row))
                col_offset += 1
                continue

            else:   # If the point has a piece
                piece = board[(col + col_offset, row)].get_contains()

                # If the piece belongs to the opponent
                if piece.get_color() != self._color:
                    self._shadows.append((col + col_offset, row))
                    break

                else:   # If the piece is the current player's
                    break

        # Check the west piece(s)
        col_offset = 1

        # Check if the next west piece is within the bounds of the board
        while 1 <= (col - col_offset) <= 9:
            # If the point is empty
            if board[(col - col_offset, row)].get_contains() is None:
                self._shadows.append((col - col_offset, row))
                col_offset += 1
                continue

            else:   # If the point has a piece
                piece = board[(col - col_offset, row)].get_contains()

                # If the piece belongs to the opponent
                if piece.get_color() != self._color:
                    self._shadows.append((col - col_offset, row))
                    break

                else:   # If the piece is the current player's
                    break


class Cannon(Piece):
    """
    Represent a cannon piece. This class is a subclass of Piece.
    """
    def __init__(self, color, col, row):
        """
        Take as parameters the cannon's color, column position, and row
        position to create a Cannon object. Initialize the corresponding data
        members, as well as the type ID.
        """
        super().__init__(color, col, row)
        self._type_id = 'N'                # Most common letter of "Cannon"

        # Initialize the list of coordinates that the cannon is shadowing
        if self._color == "red":
            self._shadows.append((col, row + 1))
            self._shadows.append((col, row + 2))
            self._shadows.append((col, row + 3))
            self._shadows.append((col, row + 4))
            self._shadows.append((col, row + 7))

        if self._color == "black":
            self._shadows.append((col, row - 1))
            self._shadows.append((col, row - 2))
            self._shadows.append((col, row - 3))
            self._shadows.append((col, row - 4))
            self._shadows.append((col, row - 7))

    def update_shadows(self, board):
        """
        Take as a parameter the current board and update the cannon's list of
        coordinates that it is shadowing.
        """
        self._shadows.clear()
        col = self._col
        row = self._row

        # Check for possible points that the cannon can move to:

        # Check the north piece(s)
        row_offset = 1

        # Check if the next north piece is within the bounds of the board
        while 1 <= (row - row_offset) <= 10:

            # If the point is empty
            if board[(col, row - row_offset)].get_contains() is None:
                self._shadows.append((col, row - row_offset))
                row_offset += 1
                continue

            # If the point has a piece, this piece becomes the "screen" over
            # which the cannon may jump to capture an opponent piece
            else:
                screen = board[(col, row - row_offset)].get_contains()
                row_offset += 1

                # Check the next piece(s) for an opponent piece
                while 1 <= (row - row_offset) <= 10:   # Check the bounds

                    # If the point is empty
                    if board[(col, row - row_offset)].get_contains() is None:
                        row_offset += 1
                        continue

                    # If the point has a piece
                    else:
                        piece = board[(col, row - row_offset)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self._color:
                            self._shadows.append((col, row - row_offset))
                            break

                        else:   # If the piece belongs to the current player
                            break
                break

        # Check the south piece(s)
        row_offset = 1

        # Check if the next south piece is within the bounds of the board
        while 1 <= (row + row_offset) <= 10:

            # If the point is empty
            if board[(col, row + row_offset)].get_contains() is None:
                self._shadows.append((col, row + row_offset))
                row_offset += 1
                continue

            # If the point has a piece, this piece becomes the "screen" over
            # which the cannon may jump to capture an opponent piece
            else:
                screen = board[(col, row + row_offset)].get_contains()
                row_offset += 1

                # Check the next piece(s) for an opponent piece
                while 1 <= (row + row_offset) <= 10:   # Check the bounds

                    # If the point is empty
                    if board[(col, row + row_offset)].get_contains() is None:
                        row_offset += 1
                        continue

                    # If the point has a piece
                    else:
                        piece = board[(col, row + row_offset)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self._color:
                            self._shadows.append((col, row + row_offset))
                            break

                        else:   # If the piece belongs to the current player
                            break
                break

        # Check the east piece(s)
        col_offset = 1

        # Check if the next east piece is within the bounds of the board
        while 1 <= (col + col_offset) <= 9:

            # If the point is empty
            if board[(col + col_offset, row)].get_contains() is None:
                self._shadows.append((col + col_offset, row))
                col_offset += 1
                continue

            # If the point has a piece, this piece becomes the "screen" over
            # which the cannon may jump to capture an opponent piece
            else:
                screen = board[(col + col_offset, row)].get_contains()
                col_offset += 1

                # Check the next piece(s) for an opponent piece
                while 1 <= (col + col_offset) <= 9:   # Check the bounds

                    # If the point is empty
                    if board[(col + col_offset, row)].get_contains() is None:
                        col_offset += 1
                        continue

                    # If the point has a piece
                    else:
                        piece = board[(col + col_offset, row)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self._color:
                            self._shadows.append((col + col_offset, row))
                            break

                        else:   # If the piece belongs to the current player
                            break
                break

        # Check the west piece(s)
        col_offset = 1

        # Check if the next west piece is within the bounds of the board
        while 1 <= (col - col_offset) <= 9:

            # If the point is empty
            if board[(col - col_offset, row)].get_contains() is None:
                self._shadows.append((col - col_offset, row))
                col_offset += 1
                continue

            # If the point has a piece, this piece becomes the "screen" over
            # which the cannon may jump to capture an opponent piece
            else:
                screen = board[(col - col_offset, row)].get_contains()
                col_offset += 1

                # Check the next piece(s) for an opponent piece
                while 1 <= (col - col_offset) <= 9:   # Check the bounds

                    # If the point is empty
                    if board[(col - col_offset, row)].get_contains() is None:
                        col_offset += 1
                        continue

                    # If the point has a piece
                    else:
                        piece = board[(col - col_offset, row)].get_contains()

                        # If the piece belongs to the opponent
                        if piece.get_color() != self._color:
                            self._shadows.append((col - col_offset, row))
                            break

                        else:   # If the piece belongs to the current player
                            break
                break


class Soldier(Piece):
    """
    Represent a soldier piece. This class is a subclass of Piece.
    """
    def __init__(self, color, col, row):
        """
        Take as parameters the soldier's color, column position, and row
        position to create a Soldier object. Initialize the corresponding data
        members, the type ID, and river_crossed, which is False while the
        Soldier has not crossed the river and True after the Soldier has
        crossed the river.
        """
        super().__init__(color, col, row)
        self._type_id = 'S'                # First letter of "Soldier"
        self._river_crossed = False

        # Initialize the list of coordinates that the soldier is shadowing
        if self._color == "red":
            self._shadows.append((col, row + 1))

        if self._color == "black":
            self._shadows.append((col, row - 1))

    def update_shadows(self, board):
        """
        Take as a parameter the current board and update the soldier's list of
        coordinates that it is shadowing.
        """
        self._shadows.clear()
        col = self._col
        row = self._row

        # Check whether the soldier has crossed the river
        if self._color == "red":     # If the soldier is red
            if self._row >= 6:
                self._river_crossed = True
            else:
                self._river_crossed = False

        if self._color == "black":   # If the soldier is black
            if self._row <= 5:
                self._river_crossed = True
            else:
                self._river_crossed = False

        # Check possible points that a red soldier might be able to move to
        if self._color == "red":

            # If the soldier has not crossed the river, it can only move and
            # capture by advancing one point
            if not self._river_crossed:

                # Check the south orthogonal piece
                if 1 <= (row + 1) <= 10:
                    if board[(col, row + 1)].get_contains() is None:
                        self._shadows.append((col, row + 1))

                    # If there is a piece on the point, check its color
                    else:
                        piece = board[(col, row + 1)].get_contains()

                        # If the piece is the opponent's
                        if piece.get_color() != self._color:
                            self._shadows.append((col, row + 1))

            # If the soldier has crossed the river, it can move and capture
            # by advancing one point and by one point horizontally
            else:
                # Check the south orthogonal piece
                if 1 <= (row + 1) <= 10:
                    if board[(col, row + 1)].get_contains() is None:
                        self._shadows.append((col, row + 1))

                    # If there is a piece on the point, check its color
                    else:
                        piece = board[(col, row + 1)].get_contains()

                        # If the piece is the opponent's
                        if piece.get_color() != self._color:
                            self._shadows.append((col, row + 1))

                # Check the east orthogonal piece
                if 1 <= (col + 1) <= 9:
                    if board[(col + 1, row)].get_contains() is None:
                        self._shadows.append((col + 1, row))

                    # If there is a piece on the point, check its color
                    else:
                        piece = board[(col + 1, row)].get_contains()

                        # If the piece is the opponent's
                        if piece.get_color() != self._color:
                            self._shadows.append((col + 1, row))

                # Check the west orthogonal piece
                if 1 <= (col - 1) <= 9:
                    if board[(col - 1, row)].get_contains() is None:
                        self._shadows.append((col - 1, row))

                    # If there is a piece on the point, check its color
                    else:
                        piece = board[(col - 1, row)].get_contains()

                        # If the piece is the opponent's
                        if piece.get_color() != self._color:
                            self._shadows.append((col - 1, row))

        # Check possible points that a black soldier might be able to move to
        if self._color == "black":

            # If the soldier has not crossed the river, it can only move and
            # capture by advancing one point
            if not self._river_crossed:

                # Check the north orthogonal piece
                if 1 <= (row - 1) <= 10:
                    if board[(col, row - 1)].get_contains() is None:
                        self._shadows.append((col, row - 1))

                    # If there is a piece on the point, check its color
                    else:
                        piece = board[(col, row - 1)].get_contains()

                        # If the piece is the opponent's
                        if piece.get_color() != self._color:
                            self._shadows.append((col, row - 1))

            # If the soldier has crossed the river, it can move and capture
            # by advancing one point and by one point horizontally
            else:
                # Check the north orthogonal piece
                if 1 <= (row - 1) <= 10:
                    if board[(col, row - 1)].get_contains() is None:
                        self._shadows.append((col, row - 1))

                    # If there is a piece on the point, check its color
                    else:
                        piece = board[(col, row - 1)].get_contains()

                        # If the piece is the opponent's
                        if piece.get_color() != self._color:
                            self._shadows.append((col, row - 1))

                # Check the east orthogonal piece
                if 1 <= (col + 1) <= 9:
                    if board[(col + 1, row)].get_contains() is None:
                        self._shadows.append((col + 1, row))

                    # If there is a piece on the point, check its color
                    else:
                        piece = board[(col + 1, row)].get_contains()

                        # If the piece is the opponent's
                        if piece.get_color() != self._color:
                            self._shadows.append((col + 1, row))

                # Check the west orthogonal piece
                if 1 <= (col - 1) <= 9:
                    if board[(col - 1, row)].get_contains() is None:
                        self._shadows.append((col - 1, row))

                    # If there is a piece on the point, check its color
                    else:
                        piece = board[(col - 1, row)].get_contains()

                        # If the piece is the opponent's
                        if piece.get_color() != self._color:
                            self._shadows.append((col - 1, row))


def main():
    """
    Run a sample game in which the black player wins.
    """
    print()
    print("Welcome to xiangqi! The red player starts the game.")
    print()
    game = XiangqiGame()
    game.print_board()


    move_1 = game.make_move('c4', 'c5')  # Red move
    print("c4-c5")
    game.print_board()

    move_2 = game.make_move('e7', 'e6')  # Black move
    print("e7-e6")
    game.print_board()

    move_3 = game.make_move('c5', 'b5')  # Red move (invalid)
    print("c5-b5")
    game.print_board()

    move_4 = game.make_move('c5', 'd5')  # Red move (invalid)
    print("c5-d5")
    game.print_board()

    move_5 = game.make_move('c5', 'c6')  # Red move
    print("c5-c6")
    game.print_board()

    move_6 = game.make_move('e6', 'd6')  # Black move (invalid)
    print("e6-d6")
    game.print_board()

    move_7 = game.make_move('e6', 'f6')  # Black move (invalid)
    print("e6-f6")
    game.print_board()

    move_8 = game.make_move('e6', 'e5')  # Black move
    print("e6-e5")
    game.print_board()

    move_9 = game.make_move('c6', 'd6')  # Red move
    print("c6-d6")
    game.print_board()

    move_10 = game.make_move('e5', 'e4')  # Black move
    print("e5-e4")
    game.print_board()

    move_11 = game.make_move('d6', 'd7')  # Red move
    print("d6-d7")
    game.print_board()

    move_12 = game.make_move('e4', 'f4')  # Black move (invalid)
    print("e4-f4")
    game.print_board()

    move_13 = game.make_move('f10', 'e9')  # Black move
    print("f10-e9")
    game.print_board()

    move_14 = game.make_move('b1', 'c3')  # Red move
    print("b1-c3")
    game.print_board()

    move_15 = game.make_move('h8', 'h1')  # Black move
    print("h8-h1")
    game.print_board()

    move_16 = game.make_move('c3', 'd5')  # Red move
    print("c3-d5")
    game.print_board()

    move_17 = game.make_move('h1', 'f1')  # Black move
    print("h1-f1")
    game.print_board()

    move_18 = game.make_move('d5', 'c7')  # Red move
    print("d5-c7")
    game.print_board()

    move_19 = game.make_move('f1', 'd1')  # Black move
    print("f1-d1")
    game.print_board()

    move_20 = game.make_move('d7', 'd8')  # Red move
    print("d7-d8")
    game.print_board()

    # Put red general in check
    move_21 = game.make_move('d1', 'a1')  # Black move
    print("d1-a1")
    game.print_board()

    move_22 = game.make_move('e1', 'f1')  # Red move (invalid)
    print("e1-f1")
    game.print_board()

    move_23 = game.make_move('e1', 'e2')  # Red move
    print("e1-e2")
    game.print_board()

    move_24 = game.make_move('i10', 'i8')  # Black move
    print("i10-i8")
    game.print_board()

    move_25 = game.make_move('d8', 'e8')  # Red move
    print("d8-e8")
    game.print_board()

    move_26 = game.make_move('i8', 'f8')  # Black move
    print("i8-f8")
    game.print_board()

    # Put black general in check
    move_27 = game.make_move('e8', 'e9')  # Red move
    print("e8-e9")
    game.print_board()

    move_28 = game.make_move('d10', 'e9')  # Black move
    print("d10-e9")
    game.print_board()

    # Set up to get red general in checkmate
    move_29 = game.make_move('i1', 'i2')  # Red move
    print("i1-i2")
    game.print_board()

    move_30 = game.make_move('a10', 'a9')  # Black move
    print("a10-a9")
    game.print_board()

    move_31 = game.make_move('i2', 'f2')  # Red move
    print("i2-f2")
    game.print_board()

    move_32 = game.make_move('a9', 'd9')  # Black move
    print("a9-d9")
    game.print_board()

    move_33 = game.make_move('f2', 'f1')  # Red move
    print("f2-f1")
    game.print_board()

    move_34 = game.make_move('d9', 'd3')  # Black move
    print("d9-d3")
    game.print_board()

    move_35 = game.make_move('f1', 'e1')  # Red move
    print("f1-e1")
    game.print_board()

    move_36 = game.make_move('f8', 'f3')  # Black move
    print("f8-f3")
    game.print_board()

    move_37 = game.make_move('c1', 'a3')  # Red move
    print("c1-a3")
    game.print_board()

    move_38 = game.make_move('a1', 'g1')  # Black move
    print("a1-g1")
    game.print_board()

    move_39 = game.make_move('b3', 'b5')  # Red move
    print("b3-b5")
    game.print_board()

    move_40 = game.make_move('g7', 'g6')  # Black move
    print("g7-g6")
    game.print_board()

    move_41 = game.make_move('h3', 'h5')  # Red move
    print("h3-h5")
    game.print_board()

    # Put red general in checkmate; black player wins
    move_42 = game.make_move('e4', 'e3')  # Black move
    print("e4-e3")
    game.print_board()


if __name__ =='__main__':
    main()