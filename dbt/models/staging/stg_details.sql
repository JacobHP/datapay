SELECT * except (externalUrl, jobUrl, jobDescription),
regexp_replace(
  regexp_replace(
      regexp_replace(
        jobDescription, 
          r'(&)([^&;]*)(;)', r'<\2>'
        ),r'\<[^<>]*\>',    ' '
      ), 
      r'\s+', ' ') as jobDescription

FROM `inbound.reed_details`
