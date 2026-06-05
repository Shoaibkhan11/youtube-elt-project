    playlist_id=get_playlist_id()
    video_ids=get_video_ids(playlist_id)
    video_data=extract_video_data(video_id_list=video_ids)
    save_to_json(video_data)