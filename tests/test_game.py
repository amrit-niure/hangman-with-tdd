from src.game import Game, MaskingMode

def test_initial_masking_word():
    # games takes three arguments, the trarget letter , number of lives given , and the masking mode. 
    # when initiated, with these arguments, it should reveal all underscores and should have 3 remaining lives.
    g = Game("Python", lives=3, masking_mode=MaskingMode.WORD)
    assert g.reveal == "______"
    assert g.remaining_lives == 3