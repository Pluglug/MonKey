from vlog import VisualLog


def visual_log_in_wonderland():
    # Pseudo debug flags
    DBG_TEA_PARTY = True
    DBG_QUEEN_OF_HEARTS = True
    DBG_CHESHIRE_CAT = True

    log = VisualLog()

    # Enable inspect
    log.enable_inspect()

    # Alice falls into Wonderland
    if DBG_TEA_PARTY:
        log.header("Alice falls into Wonderland")
        log.info("Alice follows a rabbit and falls down a hole")

    # Joining the Mad Hatter's tea party
    with log.indented():
        if DBG_TEA_PARTY:
            log.info("Alice joins the Mad Hatter's tea party")
            with log.indented():
                log.warning("Mad Hatter: 'Time doesn't move here'")

    # Meeting the Queen of Hearts
    if DBG_QUEEN_OF_HEARTS:
        log.error("Queen of Hearts: 'Off with her head!'")

    # Meeting the Cheshire Cat
    if DBG_CHESHIRE_CAT:
        log.info("Alice meets the Cheshire Cat")
        with log.indented():
            log.info("Cheshire Cat: 'We're all mad here. I'm mad. You're mad'")

    # Resetting indent and disabling inspect
    log.reset_indent()
    log.disable_inspect()

    # Deleting the instance
    del log

def visual_log_in_wonderland2():
    # Pseudo debug flags
    DBG_TEA_PARTY = True
    DBG_QUEEN_OF_HEARTS = True
    DBG_CHESHIRE_CAT = True
    DBG_MADNESS = True

    log = VisualLog()

    # Enable inspect
    log.enable_inspect()

    # Alice falls into Wonderland
    if DBG_TEA_PARTY:
        log.header("Alice falls into Wonderland")
        log.info("Alice follows a rabbit and falls down a hole")

    # Joining the Mad Hatter's tea party
    log.increase()  # Increase indentation manually
    if DBG_TEA_PARTY:
        log.info("Alice joins the Mad Hatter's tea party")

        log.increase()  # Further increase for Mad Hatter's quote
        log.warning("Mad Hatter: 'Time doesn't move here'")

    # Meeting the Queen of Hearts
    if DBG_QUEEN_OF_HEARTS:
        log.increase()  # Dramatically increasing indentation
        log.error("Queen of Hearts: 'Off with her head!'")

    # Meeting the Cheshire Cat
    if DBG_CHESHIRE_CAT:
        log.increase()  # Further increasing indentation
        log.info("Alice meets the Cheshire Cat")
        log.increase()  # Even more indentation for the cat's quote
        log.info("Cheshire Cat: 'We're all mad here. I'm mad. You're mad'")

    # Resetting indent to zero - symbolizing Alice's return to normalcy
    if DBG_MADNESS:
        log.reset_indent()  # Resetting indentation to zero
        log.header("Alice finds her way back")

    # Resetting indent and disabling inspect
    log.reset_indent()
    log.disable_inspect()

    # Deleting the instance
    del log


def visual_log_in_wonderland3():
    # Pseudo debug flags
    DBG_FOLLOW_RABBIT = True
    DBG_TEA_PARTY = True
    DBG_MEET_CATERPILLAR = False
    DBG_QUEEN_OF_HEARTS = True
    DBG_CHESHIRE_CAT = True
    DBG_FINAL_ESCAPE = True

    log = VisualLog()

    # Enable inspect
    log.enable_inspect()

    # Alice's initial fall into Wonderland
    log.header("Alice's Adventure in Wonderland")
    if DBG_FOLLOW_RABBIT:
        log.info("Alice follows a rabbit and falls down a hole")

    # Tea Party with the Mad Hatter
    with log.indented():
        if DBG_TEA_PARTY:
            log.info("Alice joins the Mad Hatter's tea party")
            log.warning("Mad Hatter: 'Time doesn't move here'")
            log.decrease()  # Decrease indent after tea party

    # Meeting the Caterpillar (Optional)
    if DBG_MEET_CATERPILLAR:
        log.increase()  # Increase indent for caterpillar section
        log.info("Alice meets a wise caterpillar")
        log.decrease()  # Decrease indent after meeting

    # Encounter with the Queen of Hearts
    with log.indented():
        if DBG_QUEEN_OF_HEARTS:
            log.error("Queen of Hearts: 'Off with her head!'")

    # Cheshire Cat provides guidance
    if DBG_CHESHIRE_CAT:
        log.increase()  # Increase indent for Cheshire Cat
        log.info("Alice meets the Cheshire Cat")
        log.info("Cheshire Cat: 'We're all mad here. I'm mad. You're mad'")
        log.decrease()  # Decrease indent after Cheshire Cat

    # Alice's final escape
    if DBG_FINAL_ESCAPE:
        log.header("Alice finds her way back")
        log.info("Alice wakes up from her dream and returns to reality")

    # Resetting indent and disabling inspect
    log.reset_indent()
    log.disable_inspect()

    # Deleting the instance
    del log


if __name__ == "__main__":
    visual_log_in_wonderland3()
