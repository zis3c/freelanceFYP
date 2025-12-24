
path = 'templates/careers/career_detail.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i in range(len(lines)):
    if skip:
        skip = False
        continue
        
    line = lines[i]
    stripped = line.strip()
    
    # Generic joiner for split tags
    # If a line ends with {{ or |filter and next line starts with value or }}
    
    # Check for split closing braces }}
    if i + 1 < len(lines) and lines[i+1].strip().startswith('}}'):
         # Check if this line has the opening {{
         if '{{' in line:
            # Join them
            merged = line.rstrip() + ' ' + lines[i+1].strip()
            # If the next line had more content after }}, append it? 
            # In our case it is usually }}</span> or }}</p>
            if lines[i+1].strip().endswith(('</span>', '</p>', '</div>')):
                 pass # It's fine
            
            new_lines.append(merged + '\n')
            skip = True
            print(f"Fixed split tag at line {i+1}: {merged.strip()}")
            continue

    # Specific check for the 'date' case where it splits after {{
    if stripped.endswith('{{') and i + 1 < len(lines) and 'review.created_at' in lines[i+1]:
        merged = line.rstrip() + ' ' + lines[i+1].strip()
        new_lines.append(merged + '\n')
        skip = True
        print(f"Fixed split date at line {i+1}: {merged.strip()}")
        continue

    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
