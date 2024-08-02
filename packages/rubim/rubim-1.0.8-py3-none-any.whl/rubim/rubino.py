from .tools import tools,jsonEror
from random import randint
from .config import config
from .client import req

class rubino:

    def __init__(self,auth:str):
        self.req = req(auth)
        config.mainPage = tools.dictFind(self.getPageList['data']['profiles'],'is_default',True)

    @property
    def getPageList(self):
        return self.req.send_request({
            "equal": False,
            "limit": 10,
            "sort": "FromMax"
        },"getProfileList")
    
    def deletePage(self,page_profile_id:str):
        return self.req.send_request({
            "model": "Profile",
            "record_id": page_profile_id,
            "profile_id": None
        },"removeRecord")
    
    def addPostViewCount(self,post_profile_id:str,post_id:str):
        return self.req.send_request({
            "post_id": post_id,
            "post_profile_id": post_profile_id
        },"addPostViewCount")

    def addPostViewTime(self,post_profile_id:str,post_id:str,duration:int,profile_id:str=None):
        return self.req.send_request({
            "duration": duration,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "profile_id": profile_id
        },"addPostViewTime")
    
    def addViewStory(self,story_profile_id:str,story_ids:list,profile_id:str=None):
        return self.req.send_request({
            "profile_id": profile_id,
            "story_ids": story_ids,
            "story_profile_id": story_profile_id
        },"addViewStory")
    
    def getPageInfoByUsername(self,username:str):
        return tools.dictFind(
            self.searchPage(username)['data']['profiles'],
            "username",username
        )
    
    def getMyPageInfo(self,profile_id:str=None):
        return self.req.send_request({
            "profile_id": profile_id
        },"getMyProfileInfo")
    
    def getPageInfo(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },"getProfileInfo")
    
    def getNewEvents(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getNewEvents")
    
    def getSuggested(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getSuggested")
    
    def getBlockedPage(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getBlockedProfiles")
    
    def getPagePosts(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },"getProfilePosts")
    
    def getRecentFollowingPosts(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getRecentFollowingPosts")
    
    def getFollowingStory(self,profile_id:str=None):
        return self.req.send_request({
            "limit": 50,
            "profile_id": profile_id
        },"getProfilesStories")
    
    def getPostLikes(self,post_profile_id:str,post_id:str,max_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "max_id": max_id,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getPostLikes")
    
    def getPostByShareLink(self,post_link:str,profile_id:str=None):
        return self.req.send_request({
            "share_string": post_link.split("/")[-1],
            "profile_id": profile_id
        },"getPostByShareLink")
    
    def getStory(self,story_profile_id:str,story_ids:list,profile_id:str=None):
        return self.req.send_request({
            "profile_id": profile_id,
            "story_ids": story_ids,
            "story_profile_id": story_profile_id
        },"getStory")

    def getStoryIds(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "profile_id": profile_id,
            "target_profile_id": target_profile_id
        },"getStoryIds")
    
    def getStoryViewers(self,story_id:str,profile_id:str=None):
        return self.req.send_request({
            "limit": 50,
            "profile_id": profile_id,
            "story_id": story_id
        },"getStoryViewers")
    
    def setStorySetting(self,story_allow_reply:str="AllFollowers",story_save_to_archive:bool=False,story_save_to_gallery:bool=False,profile_id:str=None):
        # story_allow_reply is AllFollowers or FollowersFollowBack or Off
        return self.req.send_request({
            "profile_id": profile_id,
            "story_allow_reply": story_allow_reply,
            "story_save_to_archive": story_save_to_archive,
            "story_save_to_gallery": story_save_to_archive,
            "updated_parameters": ["story_allow_reply"]
        },"setSetting")
    
    def getMyArchiveStories(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 10,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getMyArchiveStories")
    
    def getPageHighlights(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 10,
            "sort": "FromMax",
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },"getProfileHighlights")
    
    def createHighlight(self,highlight_name:str,story_ids:list,highlight_cover_picture:str,profile_id:str=None):
        highlight_cover_res = self.req.upload(highlight_cover_picture,profile_id)
        return self.req.send_request({
            "highlight_cover": {
                "highlight_file_id": highlight_cover_res[0],
                "highlight_hash_file_receive": highlight_cover_res[1],
                "type": "File"
            },
            "highlight_name": highlight_name,
            "story_ids": story_ids,
            "profile_id": profile_id
        },"addHighlight")
    
    def highlightStory(self,highlight_id:str,story_id:str,profile_id:str=None):
        return self.req.send_request({
            "highlight_id": highlight_id,
            "story_id": story_id,
            "profile_id": profile_id
        },"highlightStory")
    
    def removeStoryFromHighlight(self,highlight_id:str,remove_story_ids:list,profile_id:str=None):
        return self.req.send_request({
            "highlight_id": highlight_id,
            "remove_story_ids": remove_story_ids,
            "updated_parameters":["remove_story_ids"],
            "profile_id": profile_id
        },"editHighlight")
    
    def getHashTagTrend(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getHashTagTrend")
    
    def getExplorePosts(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 51,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getExplorePosts")
    
    def getTaggedPosts(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },"getTaggedPosts")

    def likePost(self,post_profile_id:str,post_id:str,profile_id:str=None):
        return self.req.send_request({
            "action_type": "Like",
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "track_id": "Related",
            "profile_id": profile_id
        },"likePostAction")
    
    def unlikePost(self,post_profile_id:str,post_id:str,profile_id:str=None):
        return self.req.send_request({
            "action_type": "Unlike",
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "track_id": "Related",
            "profile_id": profile_id
        },"likePostAction")

    def addComment(self,post_profile_id:str,post_id:str,text:str,profile_id:str=None):
        return self.req.send_request({
            "content": text,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "rnd": randint(100000,999999999),
            "profile_id": profile_id
        },"addComment")
    
    def deleteComment(self,post_id:str,comment_id:str,text:str,profile_id:str=None):
        return self.req.send_request({
            "model": "Comment",
            "post_id": post_id,
            "record_id": comment_id,
            "profile_id": profile_id
        },"removeRecord")
    
    def likeComment(self,comment_id:str,post_id:str,profile_id:str=None):
        return self.req.send_request({
            "action_type": "Like",
            "comment_id": comment_id,
            "post_id": post_id,
            "profile_id": profile_id
        },"likeCommentAction")
    
    def unlikeComment(self,comment_id:str,post_id:str,profile_id:str=None):
        return self.req.send_request({
            "action_type": "Unlike",
            "comment_id": comment_id,
            "post_id": post_id,
            "profile_id": profile_id
        },"likeCommentAction")
    
    def getComments(self,post_profile_id:str,post_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getComments")
    
    def requestFollow(self,followee_id:str,profile_id:str=None):
        return self.req.send_request({
            "f_type": "Follow",
            "followee_id": followee_id,
            "profile_id": profile_id
        },"requestFollow")
    
    def unFollow(self,followee_id:str,profile_id:str=None):
        return self.req.send_request({
            "f_type": "Unfollow",
            "followee_id": followee_id,
            "profile_id": profile_id
        },"requestFollow")
    
    def getPageFollower(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "f_type": "Follower",
            "limit": 50,
            "sort": "FromMax",
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },"getProfileFollowers")
    
    def getPageFollowing(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "f_type": "Following",
            "limit": 50,
            "sort": "FromMax",
            "target_profile_id": target_profile_id,
            "profile_id": profile_id
        },"getProfileFollowers")
    
    def searchFollower(self,target_profile_id:str,username:str,max_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "max_id": max_id,
            "search_type": "Follower",
            "sort": "FromMax",
            "target_profile_id": target_profile_id,
            "username": username,
            "profile_id": profile_id
        },"getProfileFollowers")
    
    def searchFollowing(self,target_profile_id:str,username:str,max_id:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "max_id": max_id,
            "search_type": "Following",
            "sort": "FromMax",
            "target_profile_id": target_profile_id,
            "username": username,
            "profile_id": profile_id
        },"getProfileFollowers")
    
    def getNewFollowRequests(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getNewFollowRequests")
    
    def acceptRequestFollow(self,request_id:str,profile_id:str=None):
        # method for private page
        return self.req.send_request({
            "action": "Accept",
            "request_id": request_id,
            "profile_id": profile_id
        },"actionOnRequest")
    
    def declineRequestFollow(self,request_id:str,profile_id:str=None):
        # method for private page
        return self.req.send_request({
            "action": "Decline",
            "request_id": request_id,
            "profile_id": profile_id
        },"actionOnRequest")
    
    def savePost(self,post_profile_id:str,post_id:str,profile_id:str=None):
        return self.req.send_request({
            "action_type": "Bookmark",
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "track_id": "Related",
            "profile_id": profile_id
        },"postBookmarkAction")
    
    def unsavePost(self,post_profile_id:str,post_id:str,profile_id:str=None):
        return self.req.send_request({
            "action_type": "Unbookmark",
            "post_id": post_id,
            "post_profile_id": post_profile_id,
            "track_id": "Related",
            "profile_id": profile_id
        },"postBookmarkAction")
    
    def getSavedPosts(self,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 51,
            "sort": "FromMax",
            "profile_id": profile_id
        },"getBookmarkedPosts")
    
    def searchPage(self,username:str,profile_id:str=None):
        return self.req.send_request({
            "equal": False,
            "limit": 50,
            "sort": "FromMax",
            "username": username,
            "profile_id": profile_id
        },"searchProfile")
    
    def blockPage(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "action": "Block",
            "blocked_id": target_profile_id,
            "profile_id": profile_id
        },"setBlockProfile")
    
    def unblockPage(self,target_profile_id:str,profile_id:str=None):
        return self.req.send_request({
            "action": "Unblock",
            "blocked_id": target_profile_id,
            "profile_id": profile_id
        },"setBlockProfile")
    
    def reportPage(self,post_id:str,reason:int=2,profile_id:str=None):
        # reason is 1 or 2 -> reason 1 = هرزنامه / reason 2 = نامناسب
        return self.req.send_request({
            "model": "Profile",
            "reason": reason,
            "record_id": post_id,
            "profile_id": profile_id
        },"setReportRecord")

    def deletePost(self,post_id:str,profile_id:str=None):
        return self.req.send_request({
            "model": "Post",
            "record_id": post_id,
            "profile_id": profile_id
        },"removeRecord")
    
    def deleteStory(self,story_id:list,profile_id:str=None):
        return self.req.send_request({
            "profile_id": profile_id,
            "story_id": story_id,
        },"deleteStory")
    
    def setPageStatus(self,profile_status:str="Private",profile_id:str=None):
        # profile_status is Private or Public
        return self.req.send_request({
            "profile_status": profile_status,
            "profile_id": profile_id
        },"updateProfile")

    def allowSendMessagePv(self,is_message_allowed:bool=False,profile_id:str=None):
        return self.req.send_request({
            "is_message_allowed": is_message_allowed,
            "profile_id": profile_id
        },"updateProfile")
    
    def editNotification(self,is_mute:bool=False,profile_id:str=None):
        return self.req.send_request({
            "is_mute": is_mute,
            "profile_id": profile_id
        },"updateProfile")
    
    def updatePagePhoto(self,prof_file:str,profile_id:str=None):
        prof_res = self.req.upload(prof_file,profile_id)
        return self.req.send_request({
            "file_id": prof_res[0],
            "hash_file_receive": prof_res[1],
            "thumbnail_file_id": prof_res[0],
            "thumbnail_hash_file_receive": prof_res[1],
            "profile_id": profile_id
        },"updateProfilePhoto")
    
    def editPost(self,post_id:str,caption:str=None,add_comment:bool=None,profile_id:str=None):
        # add_comment is True or False
        data = {
            "post_id": post_id,
            "caption": caption,
            "allow_show_comment": add_comment,
            "profile_id": profile_id
        }

        return self.req.send_request(tools.noneKeysFind(data),"updatePost")
    
    def checkRubinoUsername(self,username:str,returnBool:bool=False):
        check_res = self.req.send_request({
            "username":username
        },'checkRubinoUsername',type_method="messenger")
        if returnBool and check_res['status_det'] == "OK":
            if check_res["data"]["exist"]:
                return jsonEror.USERNAME_EXIST
            else:
                return False
        return check_res
    
    def createPage(self,username:str,name:str=None,bio:str=None):
        username_exist = self.checkRubinoUsername(username,returnBool=True)
        if not username_exist:
            return self.req.send_request({
                "bio": bio,
                "name": name,
                "username": username
            },"createPage")
        else:
            return username_exist
        
    def editPageInfo(self,username:str=None,name:str=None,bio:str=None,email:str=None,phone:str=None,website:str=None,profile_id:str=None):

        data = tools.noneKeysFind({
            "username":username,
            "website":website,
            "phone":phone,
            "email":email,
            "name": name,
            "bio":bio,
            "profile_id": profile_id
        })

        if "username" in data and profile_id != config.mainPage["id"]:
            username_exist = self.checkRubinoUsername(username,returnBool=True)
            if type(username_exist) is bool and not username_exist:
                return self.req.send_request(data,"updateProfile")
            else:
                return username_exist
        else:
            return jsonEror.PERMISSION_DENIED
    
    def addPost(self,post_file:str,caption:str=None,width:int=668,height:int=798,duration:int=27,thumbnail_file:str=None,profile_id:str=None):
        post_res = self.req.upload(post_file,profile_id)
        if type(post_res) is tuple:

            method_data = {
                "caption": caption,
                "file_id": post_res[0],
                "hash_file_receive": post_res[1],
                "height": "862" if height > 862 else str(height),
                "is_multi_file": False,
                "post_type": post_res[2],
                "rnd": randint(100000, 999999999),
                "tagged_profiles": [],
                "thumbnail_file_id": post_res[0],
                "thumbnail_hash_file_receive": post_res[1],
                "width": "848" if width > 848 else str(width),
                "profile_id": profile_id
            }

            if post_res[2] == "Video":
                tumb_res = self.req.upload(config.thumbnail if thumbnail_file is None else thumbnail_file,profile_id)

                method_data.update({
                    "duration": str(duration),
                    "snapshot_file_id": tumb_res[0],
                    "snapshot_hash_file_receive": tumb_res[1],
                    "thumbnail_file_id": tumb_res[0],
                    "thumbnail_hash_file_receive": tumb_res[1],
                })
                
            return self.req.send_request(method_data,"addPost")
        else:
            return post_res
    
    def addStory(self,story_file:str,width:int=720,height:int=1280,duration:int=27,thumbnail_file:str=None,profile_id:str=None):
        story_res = self.req.upload(story_file,profile_id)
        if type(story_res) is tuple:

            method_data = {
                'file_id': story_res[0], 
                'hash_file_receive': story_res[1], 
                'height': 1280 if height > 1280 else height, 
                'story_type': story_res[2], 
                'rnd': randint(100000, 999999999), 
                'thumbnail_file_id': story_res[0],
                'thumbnail_hash_file_receive': story_res[1],
                'width': 720 if width > 720 else width,
                'profile_id': profile_id
            }

            if story_res[2] == "Video":
                tumb_res = self.req.upload(config.thumbnail if thumbnail_file is None else thumbnail_file,profile_id)

                method_data.update({
                    "duration": str(duration),
                    "snapshot_file_id": tumb_res[0],
                    "snapshot_hash_file_receive": tumb_res[1],
                    "thumbnail_file_id": tumb_res[0],
                    "thumbnail_hash_file_receive": tumb_res[1]
                })

            return self.req.send_request(method_data,"addStory")
        else:
            return story_res