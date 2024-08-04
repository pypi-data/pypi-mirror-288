from typing import List, Union

import pygame


class Image:
    """
    A class to ease the use of Pygame's surfaces as images.
    """

    @staticmethod
    def __create_surface_from_path(file_path: str) -> pygame.Surface:
        try:
            return pygame.image.load(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"File path '{file_path}' does not exist or is inaccessible.")

    @staticmethod
    def __check_mode_and_display():
        if not pygame.display.get_init():
            raise pygame.error("pygame.display.init() has not already been called.")

        if not pygame.display.get_active():
            raise pygame.error("pygame.display.set_mode() has not already been called.")

    @staticmethod
    def create(file_path: str) -> pygame.Surface:
        """
        Create an image from the specified path.

        Parameters
        ----------
        file_path : str
            Path of the image file.
        """

        Image.__check_mode_and_display()

        return Image.__create_surface_from_path(file_path).convert_alpha()

    @staticmethod
    def create_no_alpha(file_path: str) -> pygame.Surface:
        """
        Create an image from the specified path with no alpha channel.

        Parameters
        ----------
        file_path : str
            Path of the image file.
        """

        Image.__check_mode_and_display()

        return Image.__create_surface_from_path(file_path).convert()


class Sprite:
    """A class containing method to slice sprite sheet into list of surfaces."""

    @staticmethod
    def __get_surface(surface: Union[str, pygame.Surface]) -> pygame.Surface:
        if type(surface) == str:
            return Image.create(surface)
        elif type(surface) == pygame.Surface:
            return surface
        else:
            raise TypeError("The specified object was not a Surface or a string.")

    @staticmethod
    def slice_by_columns(
        sprite_sheet: Union[str, pygame.Surface],
        sprites_count: int
    ) -> List[pygame.Surface]:
        """
        slice by columns the given sprite sheet into the specified number of surfaces.
        Example : ABCD becomes [A, B, C, D].

        Parameters
        ----------
        sprite_sheet : str or pygame.Surface
            Either a string containing the path to the sheet
            or the sheet directly as a surface.
        sprites_count : int
            Number of sprites to slice.
        """

        sprite_sheet = Sprite.__get_surface(sprite_sheet)
        width, height = sprite_sheet.get_size()
        width = width // sprites_count

        sprites = list()
        for i in range(sprites_count):
            sprite = pygame.Surface((width, height))
            sprite.blit(
                source=sprite_sheet,
                dest=(0, 0),
                area=(i * width, 0, width, height)
            )
            sprites.append(sprite)

        return sprites

    @staticmethod
    def slice_by_rows(
        sprite_sheet: Union[str, pygame.Surface],
        sprites_count: int
    ) -> List[pygame.Surface]:
        """
        slice by rows the given sprite sheet into the specified number of surfaces.
        Example :
        A
        B
        C
        D

        becomes [A, B, C, D]

        Parameters
        ----------
        sprite_sheet : str or pygame.Surface
            Either a string containing the path to the sheet
            or the sheet directly as a surface.
        sprites_count : int
            Number of sprites to slice.
        """

        sprite_sheet = Sprite.__get_surface(sprite_sheet)
        width, height = sprite_sheet.get_size()
        height = height // sprites_count

        sprites = list()
        for i in range(sprites_count):
            sprite = pygame.Surface((width, height))
            sprite.blit(
                source=sprite_sheet,
                dest=(0, 0),
                area=(0, i * height, width, height)
            )
            sprites.append(sprite)

        return sprites

    @staticmethod
    def __slice_vertically_then_horizontally(
        sprite_sheet: Union[str, pygame.Surface],
        sprites_count_width: int,
        sprites_count_height: int
    ) -> List[List[pygame.Surface]]:
        """"""

        sprites_rows = Sprite.slice_vertically(sprite_sheet, sprites_count_width)

        sprites = list()
        for row in sprites_rows:
            sprites.append(Sprite.slice_horizontally(row, sprites_count_height))

        return sprites

    @staticmethod
    def __slice_horizontally_then_vertically(
        sprite_sheet: Union[str, pygame.Surface],
        sprites_count_width: int,
        sprites_count_height: int
    ) -> List[List[pygame.Surface]]:
        """"""

        sprites_rows = Sprite.slice_horizontally(sprite_sheet, sprites_count_width)

        sprites = list()
        for row in sprites_rows:
            sprites.append(Sprite.slice_vertically(row, sprites_count_height))

        return sprites

    @staticmethod
    def slice_both_ways(
        sprite_sheet: Union[str, pygame.Surface],
        sprites_count_width: int,
        sprites_count_height: int,
        by_rows_first: bool = True
    ) -> List[List[pygame.Surface]]:
        """
        slice by rows and by columns the given sprite sheet into the specified number of surfaces.
        The order is given by the 'by_rows' parameters.

        Parameters
        ----------
        sprite_sheet : str or pygame.Surface
            Either a string containing the path to the sheet,
            or the sheet directly as a surface.
        sprites_count_width : int
            Number of sprites in each row.
        sprites_count_height : int
            Number of psrites in each column.
        by_rows : bool, default = True
            Indicates if the slice should be done first by rows (True)
            or by columns (False).
            Example :
            ABCD
            EFGH
            IJKL

            becomes [[A, B, C, D], [E, F, G, H], [I, J, K, L]] if by_rows_first is True
            and [[A, E, I], [B, F, J], [C, G, K], [D, H, L]] if by_rows_first is False.
        """

        if by_rows_first:
            return Sprite.__slice_vertically_then_horizontally(sprite_sheet, sprites_count_width, sprites_count_height)
        else:
            return Sprite.__slice_horizontally_then_vertically(sprite_sheet, sprites_count_width, sprites_count_height)
