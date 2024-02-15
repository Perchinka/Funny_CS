float iTime;
float zoomSpeed;

float4 main(in float2 uv: TEXCOORD0): SV_TARGET
{
    float zoom = pow(1.1, zoomSpeed * iTime);
    float2 z = ((3.5 * (uv - 0.5)) / zoom) + 0.05;
    float2 c = float2(0.285, 0.01);
    // float2 c = (0.285, 0.41);
    // float2 c = z;

    float max_iterations = sin(iTime) * 100.0;

    float iterations = 0.0;
    for(float i = 0.0; i < 100; i+=0.3)
    {
        float x = (z.x*z.x - z.y*z.y) + c.x;
        float y = (2*z.x*z.y) + c.y;
        z = float2(x, y);

        if(length(z) > 4.0f)
        {
            iterations = i;
            break;
        }
    }

    float3 color;
    float norm = iterations / 100.0; 
    color = float3(norm, sqrt(norm), pow(norm, 0.3));
    
    return float4(color, 1);
}