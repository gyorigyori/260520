import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="호수 물결 시뮬레이터",
    page_icon="🌊",
    layout="wide"
)

# 2. 사이드바 디자인 요소 (사용자 커스텀)
st.sidebar.header("🌊 호수 설정")
st.sidebar.write("물결의 성질을 원하는 대로 조절해보세요.")

ripple_color = st.sidebar.color_picker("물결 색상 선택", "#5dade2")
ripple_speed = st.sidebar.slider("물결 확산 속도", 1.0, 5.0, 2.5, step=0.5)
max_radius = st.sidebar.slider("물결 최대 크기 (반지름)", 50, 300, 150, step=10)
bg_color = st.sidebar.color_picker("호수 배경색 선택", "#0f172a")

# 메인 화면 설명
st.title("🌊 잔잔한 호수 물결 효과")
st.caption("아래 어두운 호수 영역을 클릭하면 돌을 던진 것처럼 동그란 물결이 퍼져나갑니다.")

# 3. HTML / CSS / JavaScript 주입 (물결 효과 구현)
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: {bg_color};
            user-select: none;
        }}
        canvas {{
            display: block;
            width: 100vw;
            height: 70vh;
            cursor: pointer;
        }}
    </style>
</head>
<body>

    <canvas id="lakeCanvas"></canvas>

    <script>
        const canvas = document.getElementById('lakeCanvas');
        const ctx = canvas.getContext('2d');

        // 캔버스 크기를 브라우저 영역에 맞춤
        function resizeCanvas() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        let ripples = [];
        const color = "{ripple_color}";
        const speed = {ripple_speed};
        const maxRadius = {max_radius};

        // 클릭 이벤트 리스너
        canvas.addEventListener('click', (e) => {{
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // 하나의 클릭에 3개의 동심원 레이어를 생성해 리얼함 추가
            ripples.push({{ x, y, radius: 0, opacity: 1 }});
        }});

        // HEX 색상을 RGBA로 변환하는 함수
        function hexToRgbA(hex, alpha) {{
            let c;
            if(/^#([A-Fa-f0-9]{3}){{1,2}}$/.test(hex)){{
                c = hex.substring(1).split('');
                if(c.length == 3){{
                    c = [c[0], c[0], c[1], c[1], c[2], c[2]];
                }}
                c = '0x' + c.join('');
                return 'rgba('+[(c>>16)&255, (c>>8)&255, c&255].join(',')+','+alpha+')';
            }}
            return 'rgba(255,255,255,'+alpha+')';
        }}

        // 애니메이션 루프
        function animate() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = ripples.length - 1; i >= 0; i--) {{
                let r = ripples[i];
                r.radius += speed;
                r.opacity = 1 - (r.radius / maxRadius);

                // 투명도가 0 이하가 되면 배열에서 제거
                if (r.opacity <= 0) {{
                    ripples.splice(i, 1);
                    continue;
                }}

                // 퍼져나가는 동심원 그리기 (물결 파형 표현을 위해 여러 겹으로 묘사)
                for (let j = 0; j < 3; j++) {{
                    let currentRadius = r.radius - (j * 20);
                    if (currentRadius > 0) {{
                        ctx.beginPath();
                        ctx.arc(r.x, r.y, currentRadius, 0, Math.PI * 2);
                        ctx.strokeStyle = hexToRgbA(color, r.opacity * (1 - j * 0.3));
                        ctx.lineWidth = 3 - j;
                        ctx.stroke();
                    }}
                }}
            }}
            requestAnimationFrame(animate);
        }}

        animate();
    </script>
</body>
</html>
"""

# Streamlit에 HTML 컴포넌트 렌더링
components.html(html_code, height=550)
