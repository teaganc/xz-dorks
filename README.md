#Why the xz exploit is EVEN worse than you think

The threat of supply chain attacks in open source software have been theorized widely however their real implications have become crystal clear in the last few days. As I am sure you are aware, a malicious actor recently succeeded in backdooring the xz project after a 2 year campaign. They gradually built trust through legitiment pull requests while at the same time posing as multiple online personas harasing the maintainer to accelerate their scheme. I encourage you to familiarize yourself before continuing as the exploitation process and how they were eventually caught as it is an unbelievable story. The primary sources are readily available and many creators have done an excellent job covering it as well.

Once you are aware of the situation, I think two conclusions aren't terribly controversial. Firstly, we as a community failed Lasse Collin, the original maintainer of the project. We need to do better at supporting the developer who are maintaining the open source projects we depend on. Secondly, our procedures of packing tarballs and distributing them need some examination.


With that in mind, let's take some time to examine the attack surface and see what can be learn to better protect ourselves.

I started out with good intentions. Ideally, I would have liked to highlight something like 100 repositories for the community to look at. I wanted to target projects with wide use, with maintainer who are over worked and under compensated, and perhaps with files or processes that could indicate other exploits of a simmilar kind could be lurking yet undiscovered. Spoilers: that didn't happen. Here is the list of over 3000 projects that seem like they could be in need of support. About 60% of projects investigated are being held up by a single or a pair of developers. Although analyzing all of those projects is beyond my reach (and github rate limits), some weak inital investigation seems to indicate many of them could potentially harbor hidden data which could be malicious.

###Polling Gentoo

There are 17986 packages by my count in the gentoo package repo as of writing. Of those, 8253 are backed by repositories on github. I'd like to investigate them all, however for the sake of simplicity we will start here. Also if you'd like to follow along the source code I will be leaving links to the files used to collect this information.

Now I'd like to know which packages are distributed to the most systems. However I can't seem to find anything like a download count for packages on any major linux distributions sites. In lieu of being able to find this information, we need some proxy indicator. Github stars might be useful here, but I took some inspiration from search engines and simply rated packages based on how many other packages depend on them. I'm sure this could easily be improved. PageRank comes to mind but let's not overcomplicate things. Here is our data at this point. On line 68 is our friend app-arch/xz-utils which is reassuring.

### Polling Github

Package popularity is important but currently the names sitting at the top of our list are things like x11, gnome, kde, opengl and jre. All of which are major projects with industry backing so not exactly what we are looking for. Also I'd be remiss to not mention ghc sitting on line 14 which would surprise me if I didn't already know that each individual library is it's own package. Regardless, it's time to start digging into the github api. Requests are limited to 5000/hr for authenticated users which is going to be a bit of a problem. We will start by retrieving the contributors. According to a headline on the top page of google there are at least 5 different ways to do this. With a little digging we can find the one that includes the number of contributions here https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-contributors. After a couple of hours of banging against rate limits I was able to pull everything down. I will leave all the data pulled from github in the repo under /repos to save you the experience.

Throwing the data into matplotlib: 

The y axis is number of packages and the x axis is the percentage of commits contributed by the top 1, 2 3 and 4 contributors cummulatively. 
```
Top 1 > 80%: 0.3768647281921618
Top 2 > 80%: 0.5849557522123894
Top 3 > 80%: 0.7173198482932996
Top 4 > 80%: 0.7978508217446271
```
We can see that for 38% of projects a single maintainer has contributed over 80% of the commits. Similarly 58% of projects the top two contributors have contributed over 80% of the commits. I am going to filter out only the projects in which over 80% of the commits are submitted by two maintainers. I believe that is what we would have seen in xz's case.  This cuts our package count to 4612.

### Cranking on Github

Another metric that is important is code frequency. Certain libraries are written and used for a long time without needing to be updated. Think of berkley sockets. I don't believe these are the kind of libraries which would be affective targets for xz-style attackers. So let's filter them out. We can grab the recent commits from github and analyse their last commit dates. Notice in the request ?per_page=1 is passed to limit the number of commits to grab per repo? Yeah I didn't and now I have over a GB of json sitting on my hard drive. Since it was taking a long time, I even remembered two more github accounts I had to parallelize the task. I guess what I am trying to say is I am sorry Github. It was an honest mistake.  Anyways, filtering out repos with no commits in the last year leaves us with 3013 repositories. These are still sorted by dependency count so those near the bottom are likely less important and the ones near the top are likely more important.

### Abusing Github

I would have liked to see less that 3000 repos in that count. I would expect then that 30-40 percent of active projects are being maintained by one or two people. Maybe those numbers are better on sites other than github and maybe the numbers are better for more popular repos but still it doesn't look great. 

At this point, I'd like to see how many of these repos contain big binary files where exploits could be hiding. As you may know, git does not allow you to view files without cloning a repository. On the brightside, github does not rate limit cloning (although they may throttle). What you may not know is that svn does allow you to view file trees without downloading anything. Luckily, I do happen to know that, as well as the fact that github actually supports svn as well as git. 

https://github.blog/2023-01-20-sunsetting-subversion-support/
```
As of January 8, 2024 (about a year from now), we will sunset Subversion support completely on GitHub.com. A release of GitHub Enterprise Server sometime in early 2024 will also remove Subversion support. Read on for more details.
```

![](https://i.gifer.com/7CCG.gif)](https://i.gifer.com/7CCG.gif)

Digging around git clone for a while I found --no-checkout which seems to be a solution. 
```
git clone --no-checkout --depth 1 https://github.com/USER/REPO
```

This seems to only download .git which was a few kilobytes when I tested on one repo. Surely we won't have a repeat of what happened for commits. You know what? Maybe I should just pull the file tree from each repo and then delete it so I don't end up eating my whole hard drive while I let this run. With that, I left for a couple hours with the script running.

Indeed, it turns out some of those clones were still over a GB and with a cursory glace, I indeed would have ran out of hard drive space. I would apologize to Github again, but if I learned anything from statistics, it is that it only takes two points to draw a trend line. Let's take a look into the file trees. 

### Analyzing files

I guess I should have mentioned that what I'm really trying to do here is determine which files are large binary file which may have slipped through the reviewing process. I believe you can get the types of files from the github api if you query them individually. Since I am trying to be a better person and also am trying to finish this project in a day I did not opt for that route. This is why I will try to use file extensions as a proxy. Anyways, most of this isn't on the repo so with a little bashing 
```
find repos/ -name file.txt | xargs cat | grep -o "\.[0-9a-zA-Z]*$" | sort | uniq | wc -l
```
It seems there are 7679 different file extension (discluding files with no extension like LICENSE or COPYING)

Throwing a -c on unique can give you a count of each word. Here are some of my favorites:
```
      3 .aei
      2 .aeiou
      2 .aeiouy
	  
	  1 .badf00d
	  1 .chacha20poly1305
	  1 .chillispot
	  
	  3279 .conf
      1 .conf1
	  24 .conf2
      2 .conf3
      1 .conf4
      1 .conf5
      1 .conf6
	  
	  1 .may2017working
	  
	  1 .microsemi
      4 .microsoft
	  
	  1 .roaringpenguin
	  
	  1 .WingCommander
```

Throwing a couple common file formats where I think you could hide data:
```
find repos -name file.txt | xargs grep -rli "png\|jpg\|jpeg\|zip\|gz\|tar\|bz\|bz2\|wma\|wmv\|mp3\|mp4\|tiff\|tga\|svg\|flac\|obj\|zlib\|gltf\|vhd\|vhdl\|xz\|xlsx" | wc -l
```
There are 1677 packages with these types of files. I think over 1000 of those matches were just jpg and png. I don't know if we should be panicing that our repo contains images so the fact that over half of the ~3000 packages we are testing here have binary files may not be the biggest deal. Still if I was an attacker it does seem like the most straightforward and obvious place to steganographically insert something no one would notice.

### Wrap up

This is just what I could accomplish in a day. The whole point of this endeavour was to give some people in the community a starting point to find repos which could use some of their time. I think I've essentially demostrated with some napkin math the extent of the problems xz exposes within the open source community. I would love for you to engage with the community and make it better. If you would like more analysis done I may be able to make some time to persue suggestions. Alternatively, if you would like to contribute your own analysis I would be interested in reading it and PRs are always welcome. 

Thanks for taking the time to read. 

















