import unittest
import accordion

class TonePlayerTest(unittest.TestCase):
    def setUp(self):
        self.midi_tone = 53
        self.player_working = accordion.TonePlayer(self.midi_tone)
        # self.player_not_working = accordion.TonePlayer(10)

    def test_creates_tone_player(self):
        self.assertEqual(self.player_working.get_midi_tone(), self.midi_tone)
        
    def test_tone_player_playes_tone(self):
        self.player_working.play_tone()
        self.assertTrue(self.player_working.player.playing)

    def test_tone_player_stops_playing_tone(self):
        self.player_working.play_tone()
        self.player_working.stop_tone()
        self.assertFalse(self.player_working.player.playing)

    def test_creates_tone_player_for_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            player_not_working = accordion.TonePlayer(10)

    def tearDown(self):
        del self.player_working