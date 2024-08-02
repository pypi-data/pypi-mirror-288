#!/bin/zsh

# Define the host and user
GIT_HOST="github.bus.zalan.do"
GIT_USER="git"
DIALOG_APP="/Library/Application Support/Dialog/Dialog.app/Contents/MacOS/Dialog"

# Find the location of the brew command
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin/"
BREW=$(command -v brew)

echo "BREW Location: ${BREW}"
if [ -n "${BREW}" ]; then
    echo "Homebrew is installed."
else
    echo "Homebrew is not installed."
    if [ -x "$DIALOG_APP" ]; then
        "$DIALOG_APP" --message "brew is not installed, please install (homebrew)[https://brew.sh/] first." --title "Error" --height 200 --width 600 --icon warning
    else
        echo "brew is not installed, please install homebrew first."
    fi
    exit 0
fi

# Fetch the SSH host key
ssh-keyscan -t ecdsa $GIT_HOST 2>/dev/null | grep $GIT_HOST >~/.ssh/known_hosts

# Check SSH connection to the Git
ssh -o StrictHostKeyChecking=no -T $GIT_USER@$GIT_HOST 2>&1 | grep "successfully authenticated" &>/dev/null

# Check the exit status of the ssh command
if [ $? -eq 1 ]; then
    echo "SSH authentication to $GIT_HOST failed."
    #/usr/local/bin/dialog --message "ssh key is not configured for git!" --title "Error" --height 200 --width 600 --icon warning
    exit 0
else
    echo "SSH authentication to $GIT_HOST succeeded."
    git config --global url."ssh://git@github.bus.zalan.do/".insteadOf "https://github.bus.zalan.do/"
    perl -e 'alarm shift; exec @ARGV' 120 brew tap --force-auto-update base-infrastructure/homebrew-taps https://github.bus.zalan.do/base-infrastructure/homebrew-taps

    # Check the exit status of the command
    if [ $? -ne 0 ]; then
        echo "The command timed out after 2 minutes or failed to execute."
        # /usr/local/bin/dialog --message "brew command error!" --title "Error" --height 200 --width 600 --icon warning
    else
        echo "The command completed before the timeout."
    fi

    brew install zalando-aws-cli
    if [ $? -ne 0 ]; then
        echo "Brew install failed"
        # /usr/local/bin/dialog --message "zalando-aws-cli installation failed!" --title "Error" --height 200 --width 600 --icon warning
    else
        cat >"/tmp/dialog.test" <<ADDTEXT
{
    "title" : "A new version of zalando-aws-cli is now installed. ",
    "titlefont" : "name=Helvetica,size=25",
    "message" :   "Please use the new zalando-aws-cli instead of zaws.\n\nA new version of zalando-aws-cli was installed that replaces the legacy zaws cli. \nSince  zalando is migrating all authentication to OKTA, the legacy zaws is deprecated and will stop working soon.\n\nHow to use zalando-aws-cli can be found [here](https://cloud.docs.zalando.net/reference/zaws/#installation).\nFAQ for Cloud Infrastructure Access with OKTA can be found [here](https://docs.google.com/document/d/12KAm8y-L3i8yeSQBe3Urd7YRwXxnFehxAZJLVv9yCq0/edit#heading=h.l19i05d6kwnx)\n\nIf you need further assistance, please contact submit an issue to [zooport](https://github.bus.zalan.do/zooport/issues/issues/new/choose)\n",
    "messagealignment" : "left",
    "messagefont" : "name=Helvetica,size=18",
    "moveable": true,
    "ontop": true,
    "button1text": "Ok",
    "centreicon": false,
    "iconsize" : "50",
    "bannerimage" : "/Library/Application Support/Zalando/images/Banner.png"
}
ADDTEXT
        if [ -x "$DIALOG_APP" ]; then
            "$DIALOG_APP" --jsonfile "/tmp/dialog.test" --width 750 --height 500
        else
            echo "zalando-aws-cli is installed."
        fi
    fi
fi
