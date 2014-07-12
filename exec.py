import os


def main():
  # artists = ['pitbull', 'eminem', 'yg', 'jason derulo', 'sage the gemini', 'trey songz', 'ty dolla sign', 'chris brown', 'drake', 'robin thicke']
  # artists = ['jason derulo', 'sage the gemini', 'trey songz', 'ty dolla sign', 'chris brown', 'drake', 'robin thicke']
  artists = ['lil wayne', 'iggy azalea']

  for i in range(len(artists)):
    os.system('node script.js ' + '"' + artists[i] + '"')

if __name__ == "__main__":
  main()
