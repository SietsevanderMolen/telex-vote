from telex import plugin
# from telex.DatabaseMixin import DatabaseMixin, DbType

import tgl
import time
import threading


class VotePlugin(plugin.TelexPlugin):
    """
    Call a vote in the chat
    """

    vote_in_progress = False
    votes_yes = 0
    votes_no = 0

    patterns = {
        "^{prefix}vote (yes|no)$": "vote",
        "^{prefix}callvote (.+)\s*(\d\d)*$": "call_vote",
    }

    usage = [
        "{prefix}vote (yes|no): vote yes or no",
    ]

    def vote(self, msg, matches):
        peer = self.bot.get_peer_to_send(msg)
        if self.vote_in_progress:
            cast_vote = matches.group(1)
            if cast_vote == "yes":
                self.votes_yes += 1
            elif cast_vote == "no":
                self.votes_no += 1
            peer.send_msg("Vote recorded", reply=msg.id, preview=False)
        else:
            peer.send_msg("No vote in progress", reply=msg.id, preview=False)

    def call_vote(self, msg, matches):
        peer = self.bot.get_peer_to_send(msg)

        if not self.vote_in_progress:
            self.vote_in_progress = True
            vote_msg = matches.group(1)
            countdown_time = matches.group(2) or 30
            if countdown_time > 600:
                countdown_time = 600

            self.timer = threading.Timer(countdown_time, self.close_vote, args=[msg, matches])
            self.timer.start()
            peer.send_msg("VOTE NOW: {}".format(vote_msg), preview=False)
        else:
            peer.send_msg("Vote already in progress", reply=msg.id, preview=False)

    def close_vote(self, msg, matches):
        peer = self.bot.get_peer_to_send(msg)
        peer.send_msg("Voting closes now! Results:\n{} voted yes\n{} voted no".format(self.votes_yes, self.votes_no), reply=msg.id, preview=False)
        self.reset_votes();


    def reset_votes(self):
        self.votes_yes = 0
        self.votes_no = 0
        self.vote_in_progress = False
