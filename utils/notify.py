from typing import Optional
import slackweb


def send_slack(text: str, url):

    # send a message
    slack = slackweb.Slack(url=url)
    slack.notify(text=str(text))


if __name__ == "__main__":

    # define dummy message
    message = "This is a test"
    url = "https://hooks.slack.com/services/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"

    send_slack(text=message, url=url)
