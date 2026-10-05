use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

-- Exports article URLs from a NetNewsWire folder into DEVONthink bookmarks.
-- Adjust the two properties below to match your setup.
property sourceFeedName : "Instapaper: PFAS" -- name of the folder in NetNewsWire to read from
property destinationGroupPath : "/PFAS_NEWS" -- group path in DEVONthink to import into

on run
	set articleURLs to {}
	set articleTitles to {}
	
	tell application "NetNewsWire"
		repeat with theAccount in accounts
			try
				repeat with theFeed in feeds of theAccount
					if name of theFeed is equal to sourceFeedName then
						repeat with theArticle in articles of theFeed
							try
								set end of articleURLs to url of theArticle
								set end of articleTitles to title of theArticle
							end try
						end repeat
					end if
				end repeat
			end try
		end repeat
	end tell
	
	if (count of articleURLs) is 0 then
		display alert "No articles found" message "No articles were found in the NetNewsWire folder \"" & sourceFeedName & "\". Check the folder name and try again."
		return
	end if
	
	tell application "DEVONthink"
		-- Creates the group path if it doesn't already exist, otherwise reuses it.
		set destinationGroup to create location destinationGroupPath
		
		repeat with i from 1 to count of articleURLs
			set theURL to item i of articleURLs
			set theTitle to item i of articleTitles
			try
				create web document from theURL name theTitle in destinationGroup
			end try
		end repeat
	end tell
	
	display notification (count of articleURLs as string) & " articles imported into DEVONthink." with title "NNW \u2192 DEVONthink"
end run
