import checker as c


print("Part1")
print(c.build_url("example.com", "/login"))
print(c.build_url("example.com", "login"))
print(c.is_https("https://example.com"))
print(c.is_https("http://example.com"))

print("Part2")
print(c.build_url("example.com", "/login"))
print(c.build_url("example.com", "login"))

print("Part2")
c.show_response("https://example.com")

print("Part3")
for site in c.SITES:
    print(c.check_site(site))

print("Part4")
c.scan_sites()

print("Part5")
for site in c.SITES:
    print(c.check_headers(site))

print("\n\n")

print("Part6")
for site in c.SITES:
    print(c.retry_check(site,4))






