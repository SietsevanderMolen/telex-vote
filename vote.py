from telex import plugin
# from telex.DatabaseMixin import DatabaseMixin, DbType

import tgl
import time


class VotePlugin(plugin.TelexPlugin):
    """
    Call a vote in the chat
    """

    vote_in_progress = False
    timer = 30
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
        if vote_in_progress:
            cast_vote = matches.group(1)
            if cast_vote == "yes":
                votes_yes += 1
            elif cast_vote == "no":
                votes_no += 1
            peer.send_msg("Vote recorded", reply=msg.id, preview=False)
        else:
            peer.send_msg("No vote in progress", reply=msg.id, preview=False)

    def call_vote(self, msg, matches):
        peer = self.bot.get_peer_to_send(msg)
        if not vote_in_progress:
            vote_msg = matches.group(1)
            self.timer = matches.group(2) or 30
            if timer > 600:
                timer = 600

            peer.send_msg("VOTE NOW: {}".format(vote_msg), preview=False)
            for i in range(timer, 0, -1):
                if i == timer/2:
                    peer.send_msg("{} seconds remaining".format(t), preview=False)
                    peer.send_msg("Intermediate results:\n{} in favour\n{} against".format(votes_yes, votes_no))
                elif i == 10:
                    peer.send_msg("{} seconds remaining".format(t), preview=False)
                elif i == 5:
                    peer.send_msg("{} seconds remaining".format(t), preview=False)

                time.sleep(1)
        else:
            peer.send_msg("Vote already in progress", reply=msg.id, preview=False)

        peer.send_msg("Voting closes now! Results:\n{} voted yes\n{} voted no".format(votes_yes, votes_no), reply=msg.id, preview=False)
