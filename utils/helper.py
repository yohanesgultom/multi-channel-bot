def str_limit(s, max, suffix='..'):
    return (s[:max] + suffix) if len(s) > max else s