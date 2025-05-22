# Bind Ctrl+k to the LLM command completion
bind -x '"\C-k": __llm_cmdcomp'

__llm_cmdcomp() {
    # Store the current command line
    local old_cmd="${READLINE_LINE}"
    local cursor_pos="${READLINE_POINT}"
    local result
    
    # Move to a new line
    echo
    
    # Get the LLM completion
    if result="$(llm cmdcomp "${old_cmd}")"; then
        # If called directly with a command, execute it
        if [ -n "${1}" ]; then
            eval "${result}"
            return
        fi
        
        # Replace the command line with the result
        READLINE_LINE="${result}"
        READLINE_POINT="${#result}"
        # Move down a line to prevent bash from overwriting output
        echo
    else
        # Restore original command on error
        READLINE_LINE="${old_cmd}"
        READLINE_POINT="${cursor_pos}"
        echo "Command completion failed" >&2
    fi
}

# Allow direct command execution
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    __llm_cmdcomp "$@"
fi
