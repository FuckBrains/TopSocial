from moviepy.editor import VideoFileClip
from moviepy.video.tools.cuts import FramesMatches


def saveVideoSummaryAsGIF(destinationDirectory, file_path, image_width):
    # Open a video file (any format should work)
    clip = VideoFileClip(file_path)

    matches = FramesMatches.from_clip(clip, 1, 1)  # loose matching

    # find the best matching pair of frames > 1.5s away
    # best = matches.filter(lambda x: x.time_span > 0.5).best()
    # Write the sequence to a GIF (with speed=30% of the original)
    final = clip.subclip(matches[0].t1, matches[0].t2).speedx(0.3)
    final.write_gif(destinationDirectory, fps=2)



    # # Downsize the clip to a width of 150px to speed up things
    # clip_small = clip.resize(width=300)
    #
    # # Find all the pairs of matching frames an return their
    # # corresponding start and end times. Takes 15-60 minutes.
    # matches = FramesMatches.from_clip(clip_small, 5, 3)
    #
    # # (Optional) Save the matches for later use.
    # # matches.save("myvideo_matches.txt")
    # # matches = FramesMatches.load("myvideo_matches.txt")
    #
    # # Filter the scenes: keep only segments with duration >1.5 seconds,
    # # where the first and last frame have a per-pixel distance < 1,
    # # with at least one frame at a distance 2 of the first frame,
    # # and with >0.5 seconds between the starts of the selected segments.
    # selected_scenes = matches.select_scenes(match_thr=1,
    #                                         min_time_span=1.5, nomatch_thr=2, time_distance=0.5)
    #
    # # The final GIFs will be 450 pixels wide
    # clip_medium = clip.resize(width=image_width)
    #
    # # Extract all the selected scenes as GIFs in folder "myfolder"
    # selected_scenes.write_gifs(clip_medium, destinationDirectory)

def best_video_frame(file_path):
    clip = VideoFileClip(file_path)
    frame = clip.get_frame(1)
    print(info(frame))
    print("cccc")


def info(object, spacing=10, collapse=1):
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print
    "\n".join(["%s %s" %
               (method.ljust(spacing),
                processFunc(str(getattr(object, method).__doc__)))
               for method in methodList])

