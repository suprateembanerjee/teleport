import cv2
import time
import argparse
import os
import glob
import socket

def stream(addr:str):
	cap = cv2.VideoCapture(addr)

	while True:
		ret, frame = cap.read()
		cv2.imshow('frame', frame)

		if cv2.waitKey(1) != -1:
			break

	cap.release()
	cv2.destroyAllWindows()

def time_capture(addr:str, t:int):

	cap = cv2.VideoCapture(addr)
	# start = time.time()
	vid_len = 0
	i = 0

	while vid_len <= t:
		ret, frame = cap.read()
		cv2.imwrite(f'./frames/{i}.jpg', frame)
		i += 1
		vid_len = i / cap.get(cv2.CAP_PROP_FPS)

	cap.release()


def stitch_video(in_path:str='./frames/', ext:str='.jpg', fps:int=60, outname:str='video.mp4'):

	filenames = sorted(glob.glob(f'{in_path}*{ext}'), key=lambda x: int(x[len(in_path):-len(ext)]))
	frames = [cv2.imread(filename) for filename in filenames]
	height, width, _ = frames[0].shape

	out = cv2.VideoWriter(f'./{outname}',cv2.VideoWriter_fourcc(*'mp4v'), fps=fps, frameSize=(width, height))
 
	for frame in frames:
	    out.write(frame)
	out.release()

def capture_stream(addr:str, t:int, continue_stream:bool=True, save_frames:bool=False, fps:int=60, outname:str='video.mp4', frameSize:tuple=(640,480)):
	
	cap = cv2.VideoCapture(addr)
	out = cv2.VideoWriter(f'./{outname}',cv2.VideoWriter_fourcc(*'mp4v'), fps=fps, frameSize=frameSize)
	vid_len = 0
	i = 0

	while continue_stream or vid_len <= t:
		ret, frame = cap.read()
		
		# stream
		cv2.imshow('frame', frame)
		
		# save frames
		if save_frames:
			cv2.imwrite(f'./frames/{i}.jpg', frame)
		
		i += 1

		# stitch
		if vid_len <= t:
			out.write(frame)

		vid_len = i / cap.get(cv2.CAP_PROP_FPS)

		if cv2.waitKey(1) != -1:
			break

	out.release()
	cap.release()
	cv2.destroyAllWindows()


# Combine Capture and Stitch

def main(addr:str):
	
	stream(addr)
	# time_capture(addr, 10)
	# stitch_video()
	# capture_stream(addr=addr, t=10)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--address', type=str, required=True, help='Address to stream from (eg. tcp://192.168.1.22:8888)')
	args = parser.parse_args()

	main(args.address)