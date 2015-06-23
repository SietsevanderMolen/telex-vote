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
    votes_yes = set()
    votes_no = set()

    patterns = {
        "^{prefix}vote (yes|no)$": "vote",
        "^{prefix}callvote (.+) (\d+)$": "call_vote",
    }

    usage = [
        "{prefix}vote (yes|no): vote yes or no",
        "{prefix}callvote kick lolke 20: call for a vote, with specified seconds timeout",
    ]

    def vote(self, msg, matches):
        peer = self.bot.get_peer_to_send(msg)
        if self.vote_in_progress:
            cast_vote = matches.group(1)
            if (msg.src.id not in self.votes_yes and
                msg.src.id not in self.votes_no):
                    if cast_vote == "yes":
                        self.votes_yes.add(msg.src.id)
                    elif cast_vote == "no":
                        self.votes_no.add(msg.src.id)
                    peer.send_msg("Vote recorded", reply=msg.id, preview=False)
            else:
                peer.send_msg("You already voted", reply=msg.id, preview=False)
        else:
            peer.send_msg("No vote in progress", reply=msg.id, preview=False)

    def call_vote(self, msg, matches):
        peer = self.bot.get_peer_to_send(msg)

        if not self.vote_in_progress:
            self.vote_in_progress = True
            vote_msg = matches.group(1)
            countdown_time = 30
            if matches.group(2):
                countdown_time = int(matches.group(2))
            if countdown_time > 600:
                countdown_time = 600

            self.timer = threading.Timer(countdown_time, self.close_vote, args=[msg, matches])
            self.timer.start()
            peer.send_msg("VOTE NOW: {}".format(vote_msg), preview=False)
        else:
            peer.send_msg("Vote already in progress", reply=msg.id, preview=False)

    def close_vote(self, msg, matches):
        peer = self.bot.get_peer_to_send(msg)
        peer.send_msg("Voting closes now! Results:\n{} voted yes\n{} voted no".format(
            len(self.votes_yes), len(self.votes_no)), reply=msg.id, preview=False)
        self.reset_votes();


    def reset_votes(self):
        self.votes_yes = set()
        self.votes_no = set()
        self.vote_in_progress = False
