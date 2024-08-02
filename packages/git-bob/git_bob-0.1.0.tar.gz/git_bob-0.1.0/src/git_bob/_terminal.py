def command_line_interface():
    import os
    import sys
    import signal

    from ._github_utilities import get_most_recent_comment_on_issue, add_comment_to_issue
    from ._ai_github_utilities import setup_ai_remark, solve_github_issue, review_pull_request, comment_on_issue
    from ._endpoints import prompt_claude, prompt_chatgpt
    from github import Github

    print("Hello")
    llm_name = os.environ.get("GIT_BOB_LLM_NAME")
    if "claude" in llm_name and os.environ.get("ANTHROPIC_API_KEY") is not None:
        print("Using claude...")
        prompt = prompt_claude
    elif "gpt" in llm_name and os.environ.get("OPENAI_API_KEY") is not None:
        print("Using gpt...")
        prompt = prompt_chatgpt
    else:
        raise NotImplementedError("Make sure to specify the environment variables GIT_BOB_LLM_NAME and corresponding API KEYs.")

    # Print out all arguments passed to the script
    print("Script arguments:")
    for arg in sys.argv[1:]:
        print(arg)

    task = sys.argv[1]

    # test if we're running in the github-CI
    running_in_github_ci = task.endswith("-action")
    task = task.replace("-action", "")

    if running_in_github_ci:
        # in case we run in the github-CI, we set a timeout of 3 minutes
        def handler(signum, frame):
            print("Process timed out")
            sys.exit(1)

        signal.signal(signal.SIGALRM, handler)
        signal.alarm(180)  # Set the timeout to 3 minutes

    repository = sys.argv[2] if len(sys.argv) > 2 else None
    issue = int(sys.argv[3]) if len(sys.argv) > 3 else None

    user, text = get_most_recent_comment_on_issue(repository, issue)

    # Check if the user is a repository member
    g = Github(os.environ.get("GITHUB_API_KEY"))
    repo = g.get_repo(repository)
    members = [member.login for member in repo.get_collaborators()]
    if user not in members:
        print("User does not have access rights.")
        member_names = ", ".join(["@" + str(m) for m in members])
        add_comment_to_issue(repository, issue, f"""
Hi @{user}, 

thanks for reaching out! Unfortunately, I'm not allowed to respond to you directly. 
I need approval from a repository member: {member_names}

Best,
git-bob
""")
        sys.exit(1)

    ai_remark = setup_ai_remark()

    if not running_in_github_ci or (("git-bob comment" in text or "git-bob solve" in text) and ai_remark not in text):
        if task == "review-pull-request":
            review_pull_request(repository, issue, prompt)
        elif (not running_in_github_ci and task == "solve-issue") or (task == "comment-on-issue" and "git-bob solve" in text):
            if prompt == prompt_claude:
                raise NotImplementedError("Solving issues using claude is currently not supported. Please use gpt instead.")
            solve_github_issue(repository, issue)
        elif task == "comment-on-issue" and ("git-bob comment" in text or not running_in_github_ci):
            comment_on_issue(repository, issue, prompt)
