import sqlite3

conn = sqlite3.connect('main.db')

c = conn.cursor()

# c.execute("""CREATE TABLE teams(
#             name text,
#             id integer,
#             abbreviation text,
#             conference_id integer,
#             division_id integer
#             ) """)

# c.execute("""CREATE TABLE players(
#             name text,
#             id integer,
#             position text
#             )""")

# c.execute("""CREATE TABLE games(
#             id integer,
#             date text,
#             home_team text,
#             home_team_id integer,
#             away_team text,
#             away_team_id integer,
#             home_team_goals integer,
#             away_team_goals integer,
#             result integer,
#             h_point_pct real,
#             h_cf_pct real,
#             h_ff_pct real,
#             h_sf_pct real,
#             h_gf_pct real,
#             h_xgf_pct real,
#             h_scf_pct real,
#             h_scsf_pct real,
#             h_scgf_pct real,
#             h_scsh_pct real,
#             h_scsv_pct real,
#             h_hdsf_pct real,
#             h_hdgf_pct real,
#             h_hdsh_pct real,
#             h_hdsv_pct real,
#             h_mdsf_pct real,
#             h_mdgf_pct real,
#             h_mdsh_pct real,
#             h_mdsv_pct real,
#             h_ldsf_pct real,
#             h_ldgf_pct real,
#             h_ldsh_pct real,
#             h_ldsv_pct real,
#             h_sh_pct real,
#             h_sv_pct real,
#             h_PDO real,
#             a_point_pct real,
#             a_cf_pct real,
#             a_ff_pct real,
#             a_sf_pct real,
#             a_gf_pct real,
#             a_xgf_pct real,
#             a_scf_pct real,
#             a_scsf_pct real,
#             a_scgf_pct real,
#             a_scsh_pct real,
#             a_scsv_pct real,
#             a_hdsf_pct real,
#             a_hdgf_pct real,
#             a_hdsh_pct real,
#             a_hdsv_pct real,
#             a_mdsf_pct real,
#             a_mdgf_pct real,
#             a_mdsh_pct real,
#             a_mdsv_pct real,
#             a_ldsf_pct real,
#             a_ldgf_pct real,
#             a_ldsh_pct real,
#             a_ldsv_pct real,
#             a_sh_pct real,
#             a_sv_pct real,
#             a_PDO real
#             )""")

# c.execute("""CREATE TABLE skater_game_data(
#             player_id integer,
#             player_name text,
#             game_id integer,
#             date text,
#             home_team name,
#             away_team name,
#             opponent_team_id integer,
#             time_on_ice real,
#             goals integer,
#             assists integer,
#             shots integer,
#             hits integer,
#             power_play_goals integer,
#             power_play_assists integer,
#             penalty_minutes integer,
#             face_off_pct real,
#             face_off_wins integer,
#             face_offs_taken integer,
#             takeaways integer,
#             giveaways integer,
#             short_handed_goals integer,
#             short_handed_assists integer,
#             blocked_shots integer,
#             plus_minus integer,
#             even_toi real,
#             pp_toi real,
#             sh_toi real
#             )""")
# c.execute("""CREATE TABLE goalie_game_data(
#             player_id integer,
#             player_name text,
#             game_id integer,
#             date text,
#             home_team name,
#             away_team name,
#             opponent_team_id integer,
#             time_on_ice real,
#             goals integer,
#             assists integer,
#             penalty_minutes integer,
#             shots_faced integer,
#             saves integer,
#             save_pct real,
#             power_play_saves integer,
#             power_play_shots_faced integer,
#             even_saves integer,
#             even_shots_faced integer,
#             short_handed_saves integer,
#             short_handed_shots_faced integer,
#             even_sv_pct real,
#             pp_sv_pct real,
#             sh_sv_pct real,
#             decision text
#             )""")

conn.commit()
conn.close()