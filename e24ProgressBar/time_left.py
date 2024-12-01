# The code of MDS_Time_Left was used.
# MDS_Time_Left
# https://github.com/cjdduarte/MDS_Time_Left

# Copyright:
#       (c) Carlos Duarte 2019-2024 <https://github.com/cjdduarte>
#       (c) Shigeyuki 2024 <https://www.patreon.com/Shigeyuki>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.



from aqt import mw

def estimateTimeLeft(total):
    try:
        config = mw.addonManager.getConfig(__name__)
        if not config.get("show_left_time", True):
            return ""

        total_seconds = 86400

        day_cutoff = getattr(mw.col.sched, "day_cutoff", getattr(mw.col.sched, "dayCutoff"))
        query_time_param = day_cutoff - total_seconds

        query = """
            SELECT count(), sum(time) / 1000
            FROM revlog
            WHERE id > ?
        """

        params = (query_time_param * 1000,)
        cards, thetime = mw.col.db.first(query, *params)

        cards = cards or 0
        thetime = thetime or 0
        speed = cards * 60 / max(1, thetime)
        minutes = int(total / max(1, speed))

        left_minutes = f" | left {minutes} min "
        return left_minutes

    except Exception as e:
        return ""